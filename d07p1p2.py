import re
import collections
import pprint
import itertools
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

#pprint.pprint(graph)

full_deps = collections.defaultdict(set)

for path in paths(reverse_graph, end_node):
    for i in range(len(path)):
        full_deps[path[i]].update(set(path[i+1:]))


def part1():
    seen = set()
    order = []
    available = set()
    keys = set(graph)
    while seen < keys:
        satisfied = {key for (key, deps) in full_deps.items() if set(deps) <= (seen | available) and key not in seen}
        available.update(satisfied)
        possible = {key for key in available if set(full_deps[key]) <= seen}
        #print(order, seen, available, possible)
        first = sorted(possible)[0]
        available.remove(first)
        order.append(first)
        seen.add(first)
    return order


def part2():
    n_workers = 5
    dur_bias = 60

    workers = [[None, None] for x in range(n_workers)]
    done = []
    busy = set()
    order = list(part1())
    queue = set(graph)
    for seconds in itertools.count(0):
        for worker in workers:
            if worker[0]:  # not idle
                worker[1] -= 1
                if worker[1] <= 0:  # done with this work
                    done.append(worker[0])
                    worker[:] = [None, None]
        eligible_work_items = sorted({
            key
            for key
            in graph
            if key not in busy
            and key not in done
            and set(done) >= set(full_deps[key])
        })
        for worker in workers:
            if not worker[0]:  # idle worker
                if eligible_work_items:  # work to be done
                    key = eligible_work_items.pop(0)
                    busy.add(key)
                    worker[0] = key
                    worker[1] = dur_bias + (ord(worker[0]) - 65) + 1  # 65 = A
        
        print(seconds, workers, done)
        if len(done) == len(order):
            break
    
if __name__ == "__main__":
    #order = part1()
    #print(''.join(order))
    part2()