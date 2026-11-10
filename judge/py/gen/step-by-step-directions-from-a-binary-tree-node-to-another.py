"""Step-By-Step Directions at n = 10^5: two 50,000-deep chains with start and dest at their
ends (long path, deep recursion), a single chain, or a random tree."""

from _shapes import level_order

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    n = 10**5
    left, right = [None] * n, [None] * n
    if shape == 0:
        left[0], right[0] = 1, 2
        a, b, nxt = 1, 2, 3
        while nxt < n:
            (left if rng.random() < 0.5 else right)[a] = nxt
            a = nxt
            nxt += 1
            if nxt < n:
                (left if rng.random() < 0.5 else right)[b] = nxt
                b = nxt
                nxt += 1
        s, d = a, b
    elif shape == 1:
        for i in range(n - 1):
            (left if rng.random() < 0.5 else right)[i] = i + 1
        s, d = (n - 1, 0) if rng.random() < 0.5 else (0, n - 1)
    else:
        free = [(0, 0), (0, 1)]
        for i in range(1, n):
            parent, side = free.pop(rng.randrange(len(free)))
            free += [(i, 0), (i, 1)]
            (left if side == 0 else right)[parent] = i
        s, d = rng.sample(range(n), 2)
    vals = list(range(1, n + 1))
    rng.shuffle(vals)
    return {"root": level_order(vals, left, right), "startValue": vals[s], "destValue": vals[d]}
