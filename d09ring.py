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
    def __init__(self, initial_value):
        self.current = cell = Cell(value=initial_value, next=None, prev=None)
        cell.next = cell.prev = cell
        self._len = 1

    def seek(self, delta):
        if delta > 0:
            for x in range(delta):
                self.current = self.current.next
        elif delta < 0:
            for x in range(-delta):
                self.current = self.current.prev

    def insert(self, rel_index, value, make_current=False):
        self.seek(rel_index)
        insert_after_cell = self.current
        cell = Cell(value=value, next=insert_after_cell.next, prev=insert_after_cell)
        insert_after_cell.next.prev = cell
        insert_after_cell.next = cell
        if make_current:
            self.current = cell
        self._len += 1
        self.verify()

    def pop(self, rel_index):
        assert self._len >= 1
        self.seek(rel_index)
        del_cell = self.current
        del_cell.next.prev = del_cell.prev
        del_cell.prev.next = del_cell.next
        self.current = del_cell.next
        del_cell.next = del_cell.prev = None

        self._len -= 1
        self.verify()
        return del_cell.value

    def __len__(self):
        return self._len

    def iter(self, back=False):
        cell = self.current
        seen = set()
        while cell not in seen:
            yield cell.value
            seen.add(cell)
            cell = (cell.prev if back else cell.next)

    def __iter__(self):
        return self.iter()

    def riter(self):
        return self.iter(back=True)

    def verify(self):
        pass


if __name__ == '__main__':
    r = Ring('1')
    r.seek(1)
    r.insert(0, '2')
    r.seek(1)
    r.insert(0, '3')
    r.seek(-1)

    print(list(r.iter()))
