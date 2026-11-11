"""Total Cost to Hire K Workers at n = 10^5 with candidates a fifth to a third of n and k up to
half of n, so scanning both candidate windows for every hire is ~5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    hi = rng.choice((10**5, 100))
    costs = [rng.randint(1, hi) for _ in range(N)]
    return {
        "costs": costs,
        "k": rng.randint(N // 3, N // 2),
        "candidates": rng.randint(N // 5, N // 3),
    }
