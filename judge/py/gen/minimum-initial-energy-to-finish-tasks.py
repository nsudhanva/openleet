"""Minimum Initial Energy to Finish Tasks with 10^5 tasks, actual <= minimum <= 10^4."""

SEEDS = 3
N = 10**5


def generate(rng):
    tasks = []
    for _ in range(N):
        actual = rng.randint(1, 10**4)
        tasks.append([actual, rng.randint(actual, 10**4)])
    return {"tasks": tasks}
