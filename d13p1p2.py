import collections
from collections import namedtuple
from itertools import count, chain

Cart = namedtuple('Cart', 'id x y dir xcount')

dirs = '^<v>'

deltas = {
    '>': (+1, 0),
    '<': (-1, 0),
    'v': (0, +1),
    '^': (0, -1),
}

dir_ccw = {dir: dirs[(dirs.index(dir) + 1) % len(dirs)] for dir in dirs}
dir_cw = {dir: dirs[(dirs.index(dir) - 1) % len(dirs)] for dir in dirs}
dir_s = {dir: dir for dir in dirs}
xmap = [dir_ccw, dir_s, dir_cw]


def read_data(filename):
    world = {}
    carts = []
    maxx = maxy = 0
    with open(filename, 'r') as infp:
        for y, line in enumerate(infp):
            for x, c in enumerate(line.rstrip()):
                maxx = max(x + 1, maxx)
                maxy = max(y + 1, maxy)
                if c in dirs:
                    carts.append(Cart(len(carts) + 1, x, y, c, 0))
                    world[x, y] = ('-' if c in '<>' else '|')
                elif c in '-|\\/+':
                    world[x, y] = c
                elif c == ' ':
                    pass
                else:
                    raise NotImplementedError(c)
    return (world, carts, (maxx, maxy))


def run_step(world, carts):
    new_carts = []
    crashes = set()

    for cart in sorted(carts, key=lambda cart: (cart.y, cart.x)):
        cid, x, y, dir, xcount = cart
        if any((c.x, c.y) == (x, y) for c in new_carts):
            crashes.add(cid)
            continue
        dx, dy = deltas[dir]
        x += dx
        y += dy
        block = world.get((x, y))
        if block == '+':
            next_dir = xmap[xcount % len(xmap)][dir]
            xcount += 1
        elif block == '/':
            next_dir = (dir_ccw if dir in '<>' else dir_cw)[dir]
        elif block == '\\':
            next_dir = (dir_ccw if dir in '^v' else dir_cw)[dir]
        elif not block:
            raise NotImplementedError('oh my')
        else:
            next_dir = dir
        new_carts.append(cart._replace(x=x, y=y, dir=next_dir, xcount=xcount))
    return (new_carts, crashes)


def draw_world(world, carts, extents):
    maxx, maxy = extents
    cart_by_coords = {(c.x, c.y): c for c in carts}
    for y in range(maxy):
        row = []
        for x in range(maxx):
            xy = (x, y)
            cart = cart_by_coords.get(xy)
            if cart:
                row.append(cart.dir)
            else:
                row.append(world.get(xy, ' '))
        print('{:03d} {}'.format(y, ''.join(row)))


def get_coords(carts):
    carts_by_coords = collections.defaultdict(list)
    for cart in carts:
        carts_by_coords[(cart.x, cart.y)].append(cart)
    return carts_by_coords

# wrong:
# 112,79
# 112,78

def main():
    world, carts, extents = read_data('input-day13.txt')
    part = 2
    for step in count(0):
        # print(step, len(carts))
        # draw_world(world, carts, extents)

        if part == 2 and len(carts) <= 1:
            print('out of carts')
            print(carts)
            print('answer =', '%d,%d' % (carts[0].x, carts[0].y))
            break

        carts, step_crashes = run_step(world, carts)

        carts_by_coords = get_coords(carts)
        crashing_ids = set(step_crashes)
        for xy, carts_in_coord in carts_by_coords.items():
            if len(carts_in_coord) > 1:
                crashing_ids.update({c.id for c in carts_in_coord})
        if crashing_ids:
            print('crash at step', step, crashing_ids)
            if part == 1:
                raise NotImplementedError('part 1 mode, stopping here')
            else:
                print('removing carts', crashing_ids)
                carts = [cart for cart in carts if cart.id not in crashing_ids]



if __name__ == '__main__':
    main()
