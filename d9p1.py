# import tqdm

from collections import Counter

import tqdm


def ringmod(a, n):
    assert a > -n
    if a < 0:
        return n + a
    return a % n


class Cell:
    __slots__ = ['value', 'next', 'prev']

    def __init__(self, *, value, next, prev):
        self.value = value
        self.next = next
        self.prev = prev

    def __str__(self):
        return '(%s%d%s)' % (
            ('< ' if self.prev else ': '),
            self.value,
            (' >' if self.next else ' :'),
        )


class Ring:
    def __init__(self):
        self.head = None
        self.tail = None
        self._len = 0

    def insert(self, index, value):
        if not self.head:  # Special case: empty
            self.tail = self.head = Cell(value=value, next=None, prev=None)
            self._len = 1
            return

        r_index = ringmod(index, len(self))
        if r_index == len(self) - 1:  # Special case: append
            return self._append(value)

        _, insert_after_cell = self._find_cell(r_index)
        cell = Cell(value=value, next=insert_after_cell.next, prev=insert_after_cell)
        if insert_after_cell.next:
            insert_after_cell.next.prev = cell
        insert_after_cell.next = cell
        self._len += 1
        self.verify()

    def _append(self, value):
        cell = Cell(value=value, next=None, prev=self.tail)
        self.tail.next = cell
        self.tail = cell
        self._len += 1
        self.verify()

    def _find_cell(self, n):
        if n == 0:
            return (None, self.head)

        if n == self._len - 1:
            return (self.tail.prev, self.tail)

        if n > self._len / 2:
            cell = self.tail
            assert not cell.next  # tail can not have next
            n_back = self._len - n
            while n_back:
                cell = cell.prev
                n_back -= 1
            return (cell, cell.next)

        prev = None
        cell = self.head
        while n:
            prev = cell
            cell = cell.next
            n -= 1
        return (prev, cell)

    def pop(self, index):
        index = ringmod(index, len(self))
        assert 0 < index <= len(self)
        prev_cell, del_cell = self._find_cell(index)
        assert prev_cell.next is del_cell
        assert del_cell.prev is prev_cell
        if del_cell.next:
            assert del_cell.next.prev is del_cell
            del_cell.next.prev = prev_cell
        prev_cell.next = del_cell.next
        if self.tail is del_cell:
            self.tail = prev_cell
        self._len -= 1
        self.verify()
        return del_cell.value

    def __len__(self):
        return self._len

    def __iter__(self):
        cell = self.head
        while cell:
            yield cell.value
            cell = cell.next

    def riter(self):
        cell = self.tail
        while cell:
            yield cell.value
            cell = cell.prev

    def verify(self):
        return
        fwd_order = list(self)
        rev_order = list(self.riter())

        assert fwd_order == rev_order[::-1], 'fwd and rev mismatch (%s != %s)' % (fwd_order, rev_order[::-1])
        assert self._len == len(fwd_order), 'len %d != fwdorder length %d' % (self._len, len(fwd_order))
        assert self._len == len(rev_order), 'len %d != revorder length %d' % (self._len, len(rev_order))


def marbulate(n_players, highest_marble_score, verbose=False):
    scores = Counter()
    player_index = 0
    ring = Ring()
    ring.insert(0, 0)
    current_marble_index = 0
    m_iter = range(1, highest_marble_score + 1)
    for marble_score in tqdm.tqdm(m_iter):
        if marble_score % 23 == 0:
            scores[player_index] += marble_score
            removal_index = ringmod(current_marble_index - 6, len(ring))
            removal_value = ring.pop(removal_index)
            scores[player_index] += removal_value
            current_marble_index = ringmod(removal_index - 1, len(ring))
        else:
            placement_index = (current_marble_index + 2) % len(ring)
            ring.insert(placement_index, marble_score)
            current_marble_index = placement_index
        if verbose:
            ring_dump = ['%s%02d' % ('*' if i == current_marble_index else ' ', v) for (i, v) in enumerate(ring)]
            print('%02d' % marble_score, 'p%s' % (player_index + 1), ' '.join(ring_dump))
        marble_score += 1
        player_index = (player_index + 1) % n_players

    high_score = scores.most_common(1)
    return high_score[0][1]


# assert marbulate(9, 25, True) == 32
# marbulate(70, 5000)
#assert marbulate(428, 72061) == 409832  # "428 players; last marble is worth 72061 points"
print(marbulate(428, 7206100))  # "428 players; last marble is worth 7206100 points"
