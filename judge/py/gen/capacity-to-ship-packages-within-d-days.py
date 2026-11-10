"""Capacity To Ship Packages at 5 * 10^4 weights: days from 1 to n, so linear search over
capacities walks up to ~2.5 * 10^7 candidates."""

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    weights = [rng.randint(1, 500) for _ in range(N)]
    days = rng.choice([1, 2, rng.randint(1, N), N])
    return {"weights": weights, "days": days}
