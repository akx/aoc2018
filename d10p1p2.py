import re
from itertools import count

obj_re = re.compile(
    r'position=<\s*(?P<x0>[-0-9]+),\s*(?P<y0>[-0-9]+)> '
    r'velocity=<\s*(?P<dx>[-0-9]+),\s*(?P<dy>[-0-9]+)>'
)

objects = []

with open('input-day10.txt', 'r') as infp:
    for line in infp:
        line_m = obj_re.match(line)
        objects.append({k: int(v) for (k, v) in line_m.groupdict().items()})


def render_frame(t):
    pixels = {}
    xs = set()
    ys = set()
    for obj in objects:
        x = obj['x0'] + obj['dx'] * t
        y = obj['y0'] + obj['dy'] * t
        pixels[x, y] = True
        xs.add(x)
        ys.add(y)
    minx = min(xs)
    miny = min(ys)
    maxx = max(xs)
    maxy = max(ys)
    return (pixels, (minx, miny), (maxx, maxy))


def draw_frame(frame):
    data, (minx, miny), (maxx, maxy) = frame
    for y in range(miny, maxy + 1):
        r = []
        for x in range(minx, maxx + 1):
            r.append('*' if data.get((x, y)) else ' ')
        print(''.join(r))


best = (1 << 63, None, None)

for t in count(0):
    _, (minx, miny), (maxx, maxy) = frame = render_frame(t)
    size = (maxx - minx) * (maxy - miny)
    if size < best[0]:
        best = (size, t, frame)
    else:  # Okay, we're growing in entropy again
        break

print(best[:2])
draw_frame(best[2])
