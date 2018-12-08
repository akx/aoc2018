data = [int(c) for c in open('input-day8.txt', 'r').read().split()]

all_nodes = []

def read_node(data, parent=None):
    snode = {'parent': parent}
    n_children = data.pop(0)
    n_meta = data.pop(0)
    snode['children'] = [read_node(data, snode) for n in range(n_children)]
    snode['meta'] = [data.pop(0) for n in range(n_meta)]
    all_nodes.append(snode)
    return snode

root_node = read_node(data)
assert not data  # ensure everything was consumed
cksum = sum(sum(n['meta']) for n in all_nodes)

print(cksum)
