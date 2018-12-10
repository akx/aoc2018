import collections

with open("input-day6.txt", "r") as infp:
    coords = [tuple(int(c) for c in s.strip().split(', ')) for i, s in enumerate(infp)]

xs, ys = zip(*coords)
minx = min(xs)
maxx = max(xs)
miny = min(ys)
maxy = max(ys)

print((minx, miny), (maxx, maxy))

def part1():
    world = {}
    for y in range(miny, maxy):
        for x in range(minx, maxx):
            closest_dst = None
            result = None
            distances = {}
            for id, (cx, cy) in enumerate(coords, 1):
                dst = abs(x - cx) + abs(y - cy)
                distances[id] = dst
            lowest_id, lowest_distance = min(distances.items(), key=lambda p: p[1])
            if list(distances.values()).count(lowest_distance) > 1:
                result = None
            else:
                result = lowest_id
            world[x, y] = result
            #print('%-2s ' % (result if result else '--'), end='')
        #print()

    infinites = set(id for ((x, y), id) in world.items() if id and (x <= minx or y <= miny or x >= maxx or y >= maxy))
    noninfinites = set(world.values()) - infinites
    sizes = collections.Counter(id for id in world.values() if id and id in noninfinites)
    print(sizes.most_common())


def part2():
    world = {}
    for y in range(miny, maxy):
        for x in range(minx, maxx):
            distances = {}
            for id, (cx, cy) in enumerate(coords, 1):
                dst = abs(x - cx) + abs(y - cy)
                distances[id] = dst
            d_sum = sum(distances.values())
            result = (d_sum < 10000)
            world[x, y] = result
    print(collections.Counter(world.values()).most_common())

if __name__ == "__main__":
    part2()