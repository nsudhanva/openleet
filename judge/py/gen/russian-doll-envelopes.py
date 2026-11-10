"""Russian Doll Envelopes at n = 10^5: random, few distinct widths (tie-handling trap), or a
long nesting chain shuffled, so an O(n^2) DP does 10^10 work."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        env = [[rng.randint(1, 10**5), rng.randint(1, 10**5)] for _ in range(N)]
    elif shape == 1:
        env = [[rng.randint(1, 50), rng.randint(1, 10**5)] for _ in range(N)]
    else:
        env = [[i + 1, i + 1 + rng.randint(0, 3)] for i in range(N)]
        env = [[w, min(h, 10**5)] for w, h in env]
        rng.shuffle(env)
    return {"envelopes": env}
