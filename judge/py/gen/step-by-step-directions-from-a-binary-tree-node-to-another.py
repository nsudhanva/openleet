"""Step-By-Step Directions at n = 10^5: two 50,000-deep chains with start and dest at their
ends (long path, deep recursion), a single chain, or a random tree."""

from _shapes import level_order, pick_shape, random_tree, zigzag_path

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    n = 10**5
    if shape == 0:
        left, right = [None] * n, [None] * n
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
        left, right = zigzag_path(rng, n)
        s, d = (n - 1, 0) if rng.random() < 0.5 else (0, n - 1)
    else:
        left, right = random_tree(rng, n, swap=False)
        s, d = rng.sample(range(n), 2)
    vals = list(range(1, n + 1))
    rng.shuffle(vals)
    return {"root": level_order(vals, left, right), "startValue": vals[s], "destValue": vals[d]}
