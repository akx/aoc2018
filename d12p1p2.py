import itertools

import tqdm


def load_data(filename):
    initial = None
    transforms = {}
    for line in open(filename):
        line = line.strip()
        if not line:
            continue
        if line.startswith('initial state:'):
            initial = [c == '#' for c in line.split(': ')[1]]
        else:
            src, dst = line.split(' => ', 1)
            src = tuple(c == '#' for c in src)
            transforms[src] = (dst == '#')
    return (initial, transforms)


def get_next_state(state, transforms):
    new_state = {}
    for i in state_range(state):
        seg = tuple([state.get(i + s, False) for s in range(-2, 3)])
        new_state[i] = transforms.get(seg)

    # Trim from left
    offset = 0
    for offset, key in enumerate(sorted(new_state)):
        if not new_state[key]:
            del new_state[key]
        else:
            break

    return (new_state, offset)


def state_range(state):
    return range(min(state) - 2, max(state) + 2)


def format_state(state):
    return ''.join(('#' if state.get(i) else '.') for i in state_range(state))


if __name__ == '__main__':
    state, transforms = load_data('input-day12.txt')
    state = dict(enumerate(state))
    desired_generation = 50_000_000_000 - 1  # - 1 since we get the correct answer for p1 when gen == 19
    offsets = []
    scores = []
    last_fmt_state = None

    for generation in range(desired_generation):
        state, offset = get_next_state(state, transforms)
        score = sum(index for (index, flag) in state.items() if flag)
        offsets.append(offset)
        scores.append(score)
        fmt_state = format_state(state)

        if generation == 19:
            print('g20 (part 1) score', score)

        if last_fmt_state == fmt_state:
            score_inc_per_generation = scores[-1] - scores[-2]
            score_at_desired_gen = score + score_inc_per_generation * (desired_generation - generation)
            print(generation, score_inc_per_generation, score_at_desired_gen)
            break

        last_fmt_state = fmt_state
