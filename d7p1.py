import re
import collections
from toposort import toposort

step_re = re.compile(r'Step (.+?) must be finished before step (.+?) can begin.')

graph = collections.defaultdict(set)
with open('example-day7.txt') as infp:
    for m in step_re.finditer(infp.read()):
        a, b = m.groups()
        graph[b].add(a)
        graph[a]  # not actually a no-op

keys = set(graph)

# Gather a total list of dependencies via toposort:
full_deps = {key: [] for key in keys}
seen = set()
for node_list in toposort(graph):
    print(node_list)
    seen.update(node_list)
    for key in keys - seen:
        full_deps[key].extend(node_list)

print(full_deps)
seen = set()
order = []
available = set()
while seen < keys:
    satisfied = {key for (key, deps) in full_deps.items() if set(deps) <= (seen | available) and key not in seen}
    available.update(satisfied)
    possible = {key for key in available if set(full_deps[key]) <= seen}
    print(order, seen, available, possible)
    first = sorted(possible)[0]
    available.remove(first)
    order.append(first)
    seen.add(first)
print(''.join(order))