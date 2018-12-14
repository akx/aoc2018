import collections
from collections import namedtuple
from itertools import count

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
    for cart in sorted(carts, key=lambda cart: (cart.y, cart.x)):
        cid, x, y, dir, xcount = cart
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
    return new_carts


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


if __name__ == '__main__':
    world, carts, extents = read_data('input-day13.txt')
    for step in count(0):
        print(step)
        draw_world(world, carts, extents)
        carts = run_step(world, carts)
        cart_coords = collections.Counter((c.x, c.y) for c in carts)
        crashes = [(xy, v) for (xy, v) in cart_coords.items() if v > 1]
        if crashes:
            print('crash at step', step)
            print(crashes)
            raise NotImplementedError('...')
