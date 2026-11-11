"""Remove Duplicates From an Unsorted Linked List at 3 * 10^4 nodes, mostly unique values, so
counting each value by walking the list costs ~10^9 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    values = rng.sample(range(1, 10**5 + 1), N)
    repeats = rng.choice((N // 100, N // 4))
    for _ in range(repeats):
        values[rng.randrange(N)] = values[rng.randrange(N)]
    return {"head": values}
