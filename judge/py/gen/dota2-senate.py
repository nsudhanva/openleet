"""Dota2 Senate at n = 10^4: a block of about 2n/3 senators of one party before n/3 of the other,
so each ban in a list simulation walks the whole first block (~n^2 / 6 steps)."""

from _shapes import pick_shape

SEEDS = 2
N = 10**4


def generate(rng):
    first, second = "RD" if pick_shape(rng) == 0 else "DR"
    big = 2 * N // 3 + rng.randint(-50, 50)
    return {"senate": first * big + second * (N - big)}
