def load_data(filename):
    initial = None
    transforms = []
    for line in open(filename):
        line = line.strip()
        if not line:
            continue
        if line.startswith('initial state:'):
            initial = [c == '#' for c in line.split(': ')[1]]
        else:
            src, dst = line.split(' => ', 1)
            transforms.append(([c == '#' for c in src], (dst == '#')))
    return (initial, transforms)


def get_next_state(state, transforms):
    new_state = {}
    for i in state_range(state):
        seg = [state.get(i + s, False) for s in range(-2, 3)]
        for src, dst in transforms:
            if seg == src:
                new_state[i] = dst
                break
        else:
            new_state[i] = False

    # Trim from left

    for key in sorted(new_state):
        if not new_state[key]:
            del new_state[key]

    return new_state


def state_range(state):
    return range(min(state) - 2, max(state) + 2)


def format_state(state):
    return ''.join(('#' if state.get(i) else '.') for i in state_range(state))


if __name__ == '__main__':
    state, transforms = load_data('input-day12.txt')
    state = dict(enumerate(state))
    print(state)
    for x in range(20):
        state = get_next_state(state, transforms)
        score = sum(index for (index, flag) in state.items() if flag)
        print('{:02d} {:4d} {}'.format(x + 1, score, format_state(state)))
