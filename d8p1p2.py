data = [int(c) for c in open('input-day8.txt', 'r').read().split()]

all_nodes = []

def read_node(data, parent=None):
    snode = {'parent': parent}
    n_children = data.pop(0)
    n_meta = data.pop(0)
    kids = snode['children'] = [read_node(data, snode) for n in range(n_children)]
    meta = snode['meta'] = [data.pop(0) for n in range(n_meta)]
    value = 0
    if kids:
        value = 0
        for kid_index_1 in meta:
            kid_index = kid_index_1 - 1
            if 0 <= kid_index < len(kids):
                value += kids[kid_index]['value']
    else:
        value = sum(meta)
    snode['value'] = value
    all_nodes.append(snode)
    return snode

root_node = read_node(data)
assert not data  # ensure everything was consumed
cksum1 = sum(sum(n['meta']) for n in all_nodes)
print(cksum1)
cksum2 = root_node['value']
print(cksum2)
