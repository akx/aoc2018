import collections
ids_to_counts = {id: collections.Counter(id) for id in open('input-day2.txt', 'r').read().splitlines()}
n_two = len(list(id for (id, c) in ids_to_counts.items() if 2 in c.values()))
n_three = len(list(id for (id, c) in ids_to_counts.items() if 3 in c.values()))
print(n_three * n_two)