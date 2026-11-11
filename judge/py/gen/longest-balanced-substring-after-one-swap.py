"""Longest Balanced Substring After One Swap at n = 2 * 10^4, mostly ones so balanced substrings
are short, and checking every substring costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    p = rng.choice((0.05, 0.1))
    return {"s": "".join("0" if rng.random() < p else "1" for _ in range(N))}
