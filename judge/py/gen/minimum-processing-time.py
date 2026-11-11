"""Minimum Processing Time with 5000 processors and 2 * 10^4 tasks, so handing each processor the
four largest remaining tasks found by scanning is ~2 * 10^8 steps against two sorts."""

SEEDS = 2
N = 5000
LIMIT = 10**9


def generate(rng):
    return {
        "processorTime": [rng.randint(0, LIMIT) for _ in range(N)],
        "tasks": [rng.randint(1, LIMIT) for _ in range(4 * N)],
    }
