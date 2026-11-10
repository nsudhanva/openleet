"""Most Profit Assigning Work with up to 10^4 jobs (profit unrelated to difficulty) and 10^4
workers, so scanning every job per worker is 10^8 steps."""

SEEDS = 3
N = 10**4


def generate(rng):
    n = rng.choice((N, rng.randint(1, N)))
    return {
        "difficulty": [rng.randint(1, 10**5) for _ in range(n)],
        "profit": [rng.randint(1, 10**5) for _ in range(n)],
        "worker": [rng.randint(1, 10**5) for _ in range(N)],
    }
