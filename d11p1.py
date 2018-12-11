import collections


def get_fuel(gsn, x, y):
    rack_id = (x + 1) + 10
    power_level = rack_id * (y + 1) + gsn
    power_level *= rack_id
    hdig = (power_level // 100) % 10
    return hdig - 5


def part1(gsn):
    grid = {}
    top_fuel = collections.Counter()
    width = height = 300
    sq_size = 3

    for y in range(width):
        for x in range(height):
            grid[x, y] = get_fuel(gsn, x, y)

    sq_l = list(range(sq_size))
    for y in range(width - sq_size):
        for x in range(height - sq_size):
            for dy in sq_l:
                for dx in sq_l:
                    top_fuel[x + 1, y + 1] += grid[x + dx, y + dy]

    return top_fuel.most_common(1)[0]


def selfcheck():
    assert get_fuel(57, 121, 78) == -5
    assert get_fuel(39, 216, 195) == 0
    assert get_fuel(71, 100, 152) == 4
    assert part1(gsn=18) == ((33, 45), 29)
    assert part1(gsn=42) == ((21, 61), 30)


if __name__ == '__main__':
    gsn = 9445
    print(part1(gsn))
