import collections

from tqdm import tqdm


def get_fuel(gsn, x, y):
    rack_id = (x + 1) + 10
    power_level = rack_id * (y + 1) + gsn
    power_level *= rack_id
    hdig = (power_level // 100) % 10
    return hdig - 5


def calc_top_fuel(grid, top_fuel, *, width, height, sq_size):
    sq_l = list(range(sq_size))
    for y in range(width - sq_size):
        for x in range(height - sq_size):
            for dy in sq_l:
                for dx in sq_l:
                    sx = x + dx
                    sy = y + dy
                    top_fuel[x + 1, y + 1] += grid[sy * width + sx]


def gen_grid(gsn, width, height):
    grid = [0] * (width * height)
    for y in range(width):
        for x in range(height):
            grid[y * width + x] = get_fuel(gsn, x, y)
    return grid


def part1(gsn, sq_size=3):
    width = height = 300
    grid = gen_grid(gsn, width, height)
    top_fuel = collections.Counter()
    calc_top_fuel(grid, top_fuel, width=width, height=height, sq_size=sq_size)
    return top_fuel.most_common(1)[0]


def part2(gsn):
    width = height = 300
    grid = gen_grid(gsn, width, height)
    top_fuel = collections.defaultdict(collections.Counter)
    for sq_size in range(1, min(width, height)):
        print(sq_size)
        calc_top_fuel(grid, top_fuel[sq_size], width=width, height=height, sq_size=sq_size)
    best_top_fuel = collections.Counter()
    for sq_size, fuels in top_fuel.items():
        for (x, y), fuel in fuels.items():
            best_top_fuel[x, y, sq_size] += fuel
    return best_top_fuel.most_common(1)[0]


def selfcheck():
    assert get_fuel(57, 121, 78) == -5
    assert get_fuel(39, 216, 195) == 0
    assert get_fuel(71, 100, 152) == 4
    assert part1(gsn=18) == ((33, 45), 29)
    assert part1(gsn=42) == ((21, 61), 30)


if __name__ == '__main__':
    gsn = 9445
    #print(part1(gsn))
    print(part2(gsn))
