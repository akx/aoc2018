# This really should be optimized to use the previously calculated
# rectangles, but since it only takes 2 minutes with Numba end-to-end
# without that, I don't much care :)

from numba import jit, prange


def get_fuel(gsn, x, y):
    rack_id = (x + 1) + 10
    power_level = rack_id * (y + 1) + gsn
    power_level *= rack_id
    hdig = (power_level // 100) % 10
    return hdig - 5


@jit(nopython=True, parallel=True)
def calc_top_fuel(grid, *, width, height, sq_size):
    top_width = width - sq_size
    top_height = height - sq_size
    top_fuel = [0] * ((top_width) * (top_height))
    for y in prange(top_height):
        for x in prange(top_width):
            for dy in prange(sq_size):
                for dx in prange(sq_size):
                    sx = x + dx
                    sy = y + dy
                    topf_off = (y * top_width + x)
                    top_fuel[topf_off] += grid[sy * width + sx]
    return top_fuel


def gen_grid(gsn, width, height):
    grid = [0] * (width * height)
    for y in range(height):
        for x in range(width):
            grid[y * width + x] = get_fuel(gsn, x, y)
    return grid


def get_best_coords_1based(top_fuel, width, height):
    best_x = best_y = 0
    best_score = None
    for y in range(height):
        for x in range(width):
            score = top_fuel[y * width + x]
            if best_score is None or score > best_score:
                best_x = x
                best_y = y
                best_score = score
    return ((best_x + 1, best_y + 1), best_score)


def part1(gsn, sq_size=3):
    width = height = 300
    grid = gen_grid(gsn, width, height)
    top_fuel = calc_top_fuel(grid, width=width, height=height, sq_size=sq_size)
    return get_best_coords_1based(top_fuel, width=(width - sq_size), height=(height - sq_size))


def part2(gsn):
    width = height = 300
    grid = gen_grid(gsn, width, height)
    top_fuel = {}
    best = {}
    for sq_size in range(1, min(width, height)):
        print(sq_size)
        top_fuel[sq_size] = calc_top_fuel(grid, width=width, height=height, sq_size=sq_size)
        best[sq_size] = get_best_coords_1based(top_fuel[sq_size], width=(width - sq_size), height=(height - sq_size))
    print(best)
    print(sorted(best.items(), key=lambda p: p[1][1]))


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
