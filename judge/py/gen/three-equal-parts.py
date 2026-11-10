"""Three Equal Parts at n = 3 * 10^4: a pattern repeated three times with differing leading
zero gaps (answer exists), all zeros, or random bits (usually [-1, -1])."""

from _shapes import pick_shape

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        plen = rng.randint(1000, 9000)
        pattern = [1] + [rng.randint(0, 1) for _ in range(plen - 1)]
        gaps = N - 3 * plen
        a = rng.randint(0, gaps)
        b = rng.randint(0, gaps - a)
        c = gaps - a - b
        arr = [0] * a + pattern + [0] * b + pattern + [0] * c + pattern
    elif shape == 1:
        arr = [0] * N
    else:
        arr = [rng.randint(0, 1) for _ in range(N)]
    return {"arr": arr}
