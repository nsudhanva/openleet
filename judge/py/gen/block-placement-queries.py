"""Block Placement Queries at 1.5 * 10^5 queries over coordinates up to 5 * 10^4: obstacles at
distinct free positions mixed with placement checks, so scanning obstacles per query is
quadratic."""

SEEDS = 2
Q = 15 * 10**4
LIM = 5 * 10**4


def generate(rng):
    free = list(range(1, LIM + 1))
    rng.shuffle(free)
    share = rng.choice([0.2, 0.33])
    queries = []
    for _ in range(Q - 1):
        if free and rng.random() < share:
            queries.append([1, free.pop()])
        else:
            x = rng.randint(1, LIM)
            queries.append(
                [2, x, rng.randint(1, min(x, 2000)) if rng.random() < 0.8 else rng.randint(1, LIM)]
            )
    queries.append([2, LIM, rng.randint(1, LIM)])
    return {"queries": queries}
