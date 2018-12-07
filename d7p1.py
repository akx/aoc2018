import re
import collections
import pprint
from paths import paths

step_re = re.compile(r'Step (.+?) must be finished before step (.+?) can begin.')

graph = collections.defaultdict(set)
reverse_graph = collections.defaultdict(set)
with open('input-day7.txt') as infp:
    for m in step_re.finditer(infp.read()):
        a, b = m.groups()
        graph[a].add(b)
        graph[b]  # not actually a no-op
        reverse_graph[b].add(a)
        reverse_graph[a]

start_node = [key for (key, deps) in reverse_graph.items() if not deps][0]
end_node = [key for (key, deps) in graph.items() if not deps][0]

keys = set(graph)

pprint.pprint(graph)

full_deps = collections.defaultdict(set)

for path in paths(reverse_graph, end_node):
    for i in range(len(path)):
        full_deps[path[i]].update(set(path[i+1:]))

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