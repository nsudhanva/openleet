"""Number of Ways to Select Buildings at 10^5 buildings, so counting the buildings on both sides
of every middle one afresh costs 10^10 steps, 10^10 bytes even at str.count speed."""

SEEDS = 2
N = 10**5


def generate(rng):
    ones = rng.uniform(0.2, 0.8)
    return {"s": "".join("1" if rng.random() < ones else "0" for _ in range(N))}
