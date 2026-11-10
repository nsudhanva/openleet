"""Two City Scheduling at the maximum 100 people with costs up to 1000, many ties in the
cost difference."""

SEEDS = 2
N = 100


def generate(rng):
    if rng.random() < 0.5:
        costs = [[rng.randint(1, 1000), rng.randint(1, 1000)] for _ in range(N)]
    else:
        costs = []
        for _ in range(N):
            a = rng.randint(1, 990)
            costs.append([a, a + rng.choice([-1, 0, 5, 10]) if a > 1 else a + 5])
    return {"costs": costs}
