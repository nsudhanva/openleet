"""String Transformation at n = 5 * 10^5 with k near 10^15: s is a short block repeated (many
rotations match t) or all one letter but the last, so testing each rotation by building and
comparing it is ~2.5 * 10^11 character steps."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 5 * 10**5
K = 10**15


def generate(rng):
    if rng.random() < 0.5:
        block = random_string(rng, "ab", rng.choice((2, 4, 5, 8, 10)))
        s = block * (N // len(block))
    else:
        c, d = rng.sample(ascii_lowercase, 2)
        s = c * (N - 1) + d
    r = rng.randrange(1, N)
    return {"s": s, "t": s[r:] + s[:r], "k": rng.randint(K // 2, K)}
