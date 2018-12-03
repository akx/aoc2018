import re
import types
import collections
import itertools

r_re = re.compile('#(?P<id>.+?) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)')
claims = [
    types.SimpleNamespace(**{k: int(v) for (k, v) in m.groupdict().items()})
    for m
    in r_re.finditer(open('input-day3.txt', 'r').read())
]
cmap = collections.defaultdict(set)
for claim in claims:
    for x in range(claim.x, claim.x + claim.w):
        for y in range(claim.y, claim.y + claim.h):
            cmap[x, y].add(claim.id)

print(sum(1 for (xy, n) in cmap.items() if len(n) >= 2))
overlappees = set(itertools.chain(*(n for (xy, n) in cmap.items() if len(n) >= 2)))
print(set(claim.id for claim in claims) - overlappees)