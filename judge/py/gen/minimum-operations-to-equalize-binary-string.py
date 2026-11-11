"""Minimum Operations to Equalize Binary String at length 3 * 10^4 with k near n / 2, so a BFS over
zero counts that lists all ~k successors of each count is quadratic. One seed has no answer (k
even, an odd number of zeros); the others need several rounds with k even and odd."""

from _shapes import pick_shape

SEEDS = 3
N = 3 * 10**4
SPREAD = 100


def generate(rng):
    shape = pick_shape(rng)
    k = N // 2 + rng.randrange(-SPREAD, SPREAD)
    if k % 2 != (shape == 2):
        k += 1
    zeros = rng.randrange(1, N - 1)
    if k % 2 == 0 and zeros % 2 != (shape == 0):
        zeros += 1
    chars = ["0"] * zeros + ["1"] * (N - zeros)
    rng.shuffle(chars)
    return {"s": "".join(chars), "k": k}
