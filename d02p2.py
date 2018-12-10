ids = list(open('input-day2.txt', 'r').read().splitlines())

for i, a in enumerate(ids):
    for b in ids[i+1:]:
        nd = 0
        for ca, cb in zip(a, b):
            if ca != cb:
                nd += 1
            if nd > 1:
                break
        if nd == 1:
            print(''.join(c for c in a if c in b))

