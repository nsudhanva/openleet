"""Longest Well-Performing Interval at n = 10^4 days, 45% of them tiring, so the running balance
drifts down and checking every interval is the full ~5 * 10^7 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    hours = [rng.randint(9, 16) if rng.random() < 0.45 else rng.randint(0, 8) for _ in range(N)]
    return {"hours": hours}
