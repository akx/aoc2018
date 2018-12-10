from multiprocessing.pool import Pool

def depolymerize_pass(data):
    data = list(data)
    i = 0
    while i < len(data) - 1:
        ca = data[i]
        cb = data[i + 1]
        if ca != cb and ca.lower() == cb.lower():
            data[i : i + 2] = []
            continue
        i += 1
    return ''.join(data)


def depolymerize_full(data):
    while True:
        new_data = depolymerize_pass(data)
        if new_data == data:
            break
        data = new_data
    return new_data


def clean_and_depolymerize(data, unit):
    print(unit)
    cleaned_data = data.replace(unit, '').replace(unit.upper(), '')
    return (unit, depolymerize_full(cleaned_data))


def part1(input_data):
    print('->', len(depolymerize_full(input_data)))


def part2(input_data):
    units = sorted(set(c.lower() for c in input_data))
    with Pool() as p:
        clean_map = dict(p.starmap(clean_and_depolymerize, [(input_data, unit) for unit in units], chunksize=5))

    for unit, clean_length in sorted(clean_map.items(), key=lambda p: len(p[1])):
        print(unit, len(clean_length))


if __name__ == "__main__":
    input_data = open('input-day5.txt', 'r').read().strip()
    #part1(input_data)
    #part2(input_data)