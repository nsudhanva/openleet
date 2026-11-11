"""Mice and Cheese at n = 2 * 10^4 with k near n / 2, so a knapsack over (cheese, count) costs
~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {
        "reward1": [rng.randint(1, 1000) for _ in range(N)],
        "reward2": [rng.randint(1, 1000) for _ in range(N)],
        "k": rng.randint(N // 3, 2 * N // 3),
    }
