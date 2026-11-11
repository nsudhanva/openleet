"""Restore The Array at n = 10^4 digits with k near 10^9, so trying every earlier split point for
each position, instead of only the last ten, costs ~5 * 10^7 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    digits = [rng.choice("123456789")]
    while len(digits) < N:
        digits.append("0" if digits[-1] != "0" and rng.random() < 0.05 else rng.choice("123456789"))
    return {"s": "".join(digits), "k": rng.randint(10**8, 10**9)}
