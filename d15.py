import io
import time
from collections import namedtuple
from dataclasses import dataclass
from itertools import count
from typing import List, Iterable, Set

import rbg_astar

puzzle_input = """
################################
#######################.########
#######################.########
########..#############.########
#######.....#########....#..####
#######.....##########......####
######....#..########.......#..#
#######.G...########...........#
####..GG....G######..........###
########....G..###..E.......#.E#
########...G..#....G..G.....E..#
########...G...G.G...........E.#
####....G.....#####..E......#E.#
####.####.#..#######....G.....##
####.G#####.#########..........#
####G#####..#########..........#
####.####..E#########..........#
####...#..#.#########.G........#
####.....G..#########.........##
####..G....E.#######........####
####G.........#####...##....####
#####G................###..E####
#####..####...............######
####..#####.............########
#####.#######...........########
#####.########.........#########
#####.########.....E..##########
#.....#########...#.############
#..#############....############
################....############
##################.#############
################################
""".strip()

example_input = """
#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
####### 
""".strip()

Coordinate = namedtuple('Coordinate', ('x', 'y'))


@dataclass
class Unit:
    id: int
    coords: Coordinate
    side: str
    hp: int = 200
    ap: int = 3

    @property
    def x(self):
        return self.coords.x

    @property
    def y(self):
        return self.coords.y

    def __str__(self):
        return f'{self.side} unit {self.id} at {self.coords} ({self.hp} HP)'


class World:
    def __init__(self, walls: Set[Coordinate]):
        self.walls = walls
        self.width = max(c.x for c in walls) + 1
        self.height = max(c.y for c in walls) + 1


def read_input(infp):
    walls = set()
    units = []
    for y, line in enumerate(infp):
        line = line.strip()
        for x, c in enumerate(line):
            if c == '#':
                walls.add(Coordinate(x, y))
            elif c == '.':
                continue
            elif c in 'EG':
                units.append(Unit(id=len(units), coords=Coordinate(x, y), side=c))
            else:
                raise NotImplementedError((x, y, c))
    return (World(walls), units)


def reading_order(coordinable):
    return (coordinable.y, coordinable.x)


def is_open(world: World, units, x, y):
    xy = (x, y)
    if xy in world.walls or any((u.x, u.y) == xy for u in units):
        return False
    return True


def adjacent(x, y):
    u = (x, y - 1)
    d = (x, y + 1)
    l = (x - 1, y)
    r = (x + 1, y)
    yield from (u, r, d, l)


def adjacent_open(world, units, x, y):
    for c in adjacent(x, y):
        if is_open(world, units, c[0], c[1]):
            yield c


@dataclass
class Path:
    target: Unit
    start: tuple
    end: tuple
    path: list

    @property
    def length(self):
        return len(self.path)

    @property
    def first_move(self):
        assert self.path[0] == self.start
        return self.path[1]


def draw(world: World, units: Iterable[Unit]):
    for y in range(world.height):
        row = []
        for x in range(world.width):
            char = '.'
            coord = (x, y)
            if coord in world.walls:
                char = '#'
            else:
                cell_units = [unit for unit in units if unit.coords == coord]
                assert len(cell_units) <= 1
                if cell_units:
                    char = cell_units[0].side
            row.append(char)
        print('{:2d} {}'.format(y, ''.join(row)))


def part1():
    world, units = read_input(io.StringIO(example_input))
    for round in count(1):
        print('=' * 80)
        print(f'Round {round}')
        draw(world, units)
        input('Run turn?')

        for unit in sorted(units, key=reading_order):
            targets = [other_unit for other_unit in units if other_unit.side != unit.side]
            if not targets:
                raise RuntimeError(f'Combat ends at round {round}')
            targets_in_range = [
                other_unit
                for other_unit
                in units
                if unit.coords in adjacent(other_unit.x, other_unit.y)
            ]
            if targets_in_range:
                next_target = min(targets_in_range, key=lambda target: (target.hp, reading_order(target)))
                print(unit, '⚔️', next_target)
                next_target.hp -= unit.ap
            else:
                next_move_path = get_next_move(world, units, unit, targets)
                print(unit, '->', next_move_path, 'to find', next_move_path.target)
                unit.coords = next_move_path.first_move
        units = [unit for unit in units if unit.hp > 0]


def get_next_move(world: World, units: List[Unit], unit: Unit, targets) -> Path:
    grid = rbg_astar.SquareGrid(world.width, world.height)
    grid.walls.update(world.walls)
    grid.walls.update(u.coords for u in units if u != unit)
    start = unit.coords
    possible_paths = []
    for target in targets:
        for goal in adjacent_open(world, units, target.x, target.y):
            came_from, cost_so_far = rbg_astar.dijkstra_search(grid, start, goal)
            path = rbg_astar.reconstruct_path(came_from, start, goal)
            if path[-1] == goal:
                possible_paths.append(Path(
                    target=target,
                    start=start,
                    end=goal,
                    path=[Coordinate(*p) for p in path],
                ))
    # sort possible paths by distance
    possible_paths.sort(key=lambda path: path.length)
    shortest_paths = [path for path in possible_paths if path.length == possible_paths[0].length]
    # choose the next possible move by reading order
    next_move_path = min(shortest_paths, key=lambda path: path.first_move)
    assert next_move_path.first_move in set(adjacent(unit.x, unit.y)), 'next move not in adjacent'  # sanity check
    return next_move_path


if __name__ == '__main__':
    part1()
