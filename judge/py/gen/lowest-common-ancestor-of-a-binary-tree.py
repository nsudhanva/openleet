"""Lowest Common Ancestor in a binary tree of 10^5 unique values: a random tree, or a deep
caterpillar (long spine with short branches) with p and q far down."""

from _shapes import level_order, random_tree, zigzag_path

SEEDS = 2
N = 10**5
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.5:
        left, right = random_tree(rng, N)
        p, q = rng.sample(range(N), 2)
    else:
        spine = N // 2
        left, right = zigzag_path(rng, spine)
        left += [None] * (N - spine)
        right += [None] * (N - spine)
        for i in range(spine, N):
            host = i - spine
            if left[host] is None:
                left[host] = i
            else:
                right[host] = i
        p = rng.randrange(spine - 1000, spine)
        q = rng.randrange(N - 1000, N)
    val = rng.sample(range(-LIMIT, LIMIT + 1), N)
    return {"root": level_order(val, left, right), "p": val[p], "q": val[q]}
