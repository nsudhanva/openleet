"""Most Profit Assigning Work with 10^4 jobs and 10^4 workers; scanning all jobs per worker is
10^8 steps. Profit is unrelated to difficulty."""

SEEDS = 3
N = 10**4


def generate(rng):
    n = rng.choice((N, rng.randint(1, N)))
    return {
        "difficulty": [rng.randint(1, 10**5) for _ in range(n)],
        "profit": [rng.randint(1, 10**5) for _ in range(n)],
        "worker": [rng.randint(1, 10**5) for _ in range(N)],
    }
