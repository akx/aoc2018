from collections import Counter


def ringmod(a, n):
    assert a > -n
    if a < 0:
        return n + a
    return a % n


def marbulate(n_players, highest_marble_score):
    scores = Counter()
    marble_score = 1
    player_index = 0
    ring = [0]
    current_marble_index = 0
    while marble_score <= highest_marble_score:
        if marble_score % 23 == 0:
            scores[player_index] += marble_score
            removal_index = ringmod(current_marble_index - 6, len(ring))
            removal_value = ring.pop(removal_index)
            scores[player_index] += removal_value
            current_marble_index = ringmod(removal_index - 1, len(ring))
        else:
            placement_index = (current_marble_index + 2) % len(ring)
            ring.insert(placement_index + 1, marble_score)
            current_marble_index = placement_index
        marble_score += 1
        player_index = (player_index + 1) % n_players
    high_score = scores.most_common(1)
    print(high_score)


#marbulate(9, 25)
marbulate(428, 72061)  # "428 players; last marble is worth 72061 points"
