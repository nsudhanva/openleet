"""Most Profit Assigning Work at the maximum 10^4 jobs and 10^4 workers of low ability, with profit
rising with difficulty (shuffled within blocks of 100), so scanning every job per worker, or
scanning jobs from the most profitable down, is ~10^8 steps."""

SEEDS = 2
N = 10**4
BLOCK = 100
WORKER_TOP = 2 * 10**4


def generate(rng):
    difficulty = sorted(rng.randint(1, 10**5) for _ in range(N))
    profit = sorted(rng.randint(1, 10**5) for _ in range(N))
    for i in range(0, N, BLOCK):
        block = profit[i : i + BLOCK]
        rng.shuffle(block)
        profit[i : i + BLOCK] = block
    jobs = list(zip(difficulty, profit, strict=True))
    rng.shuffle(jobs)
    return {
        "difficulty": [d for d, _ in jobs],
        "profit": [p for _, p in jobs],
        "worker": [rng.randint(1, WORKER_TOP) for _ in range(N)],
    }
