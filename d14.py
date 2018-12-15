from itertools import islice, count


def print_scoreboard(scoreboard, p0, p1):
    def fnum(i, n):
        n = str(n)
        if i == p0:
            n = '(%s)' % n
        if i == p1:
            n = '[%s]' % n
        return n.center(5)

    print(''.join(fnum(i, n) for (i, n) in enumerate(scoreboard)))


def choc(input, verbose=False):
    scoreboard = seqn(input)
    yield from scoreboard
    p0 = 0
    p1 = 1
    while True:
        if verbose:
            print_scoreboard(scoreboard, p0, p1)
        new_score = scoreboard[p0] + scoreboard[p1]
        new_values = seqn(str(new_score))
        yield from new_values
        scoreboard.extend(new_values)
        p0 = (p0 + scoreboard[p0] + 1) % len(scoreboard)
        p1 = (p1 + scoreboard[p1] + 1) % len(scoreboard)
    # return


def seqn(input):
    return [int(c) for c in input]


def nseq(c):
    return ''.join(str(n) for n in c)


def selftest():
    assert nseq(islice(choc('37'), 9, 19)) == '5158916779'
    assert nseq(islice(choc('37'), 5, 15)) == '0124515891'
    assert nseq(islice(choc('37'), 18, 28)) == '9251071085'
    assert nseq(islice(choc('37'), 2018, 2028)) == '5941429882'


def part1(input):
    print(nseq(islice(choc('37'), input, input + 10)))


def part2(input):
    input = seqn(str(input))
    buf = []
    gen = choc('37')
    while True:
        buf.append(next(gen))
        if buf[-6:] == input:
            print(len(buf) - 6)
            break


if __name__ == '__main__':
    selftest()
    print('part 1')
    part1(170641)
    print('part 2')
    part2(170641)
