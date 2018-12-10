from collections import Counter

import tqdm

from d9ring import Ring


def marbulate(n_players, highest_marble_score, verbose=False):
    scores = Counter()
    player_index = 0
    ring = Ring(0)
    m_iter = range(1, highest_marble_score + 1)
    for marble_score in tqdm.tqdm(m_iter):
        if marble_score % 23 == 0:
            scores[player_index] += marble_score
            removal_value = ring.pop(-7)
            scores[player_index] += removal_value
        else:
            ring.insert(+1, marble_score, make_current=True)
        if verbose:
            ring_dump = ['%s%02d' % ('*' if v == ring.current.value else ' ', v) for (i, v) in enumerate(ring)]
            print('%02d' % marble_score, 'p%s' % (player_index + 1), ' '.join(ring_dump))
        marble_score += 1
        player_index = (player_index + 1) % n_players

    high_score = scores.most_common(1)
    return high_score[0][1]


assert marbulate(9, 25, True) == 32
assert marbulate(428, 72061) == 409832  # "428 players; last marble is worth 72061 points"
print(marbulate(428, 7206100))  # "428 players; last marble is worth 7206100 points"
