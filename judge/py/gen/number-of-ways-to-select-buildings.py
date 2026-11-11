"""Number of Ways to Select Buildings at 2 * 10^4 buildings, so counting the buildings on both sides
of every middle one afresh costs 4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    ones = rng.uniform(0.2, 0.8)
    return {"s": "".join("1" if rng.random() < ones else "0" for _ in range(N))}
