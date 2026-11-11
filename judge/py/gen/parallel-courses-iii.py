"""Parallel Courses III at the maximum 5 * 10^4 courses and relations: one shuffled chain through
every course plus a shortcut, listed against topological order, so relaxing all relations until
nothing changes takes 5 * 10^4 passes (~2.5 * 10^9 steps)."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    order = rng.sample(range(1, N + 1), N)
    relations = [[order[i], order[i + 1]] for i in range(N - 2, -1, -1)]
    a = rng.randrange(N - 2)
    relations.insert(rng.randrange(N), [order[a], order[rng.randrange(a + 2, N)]])
    time = [rng.randint(1, 10**4) for _ in range(N)]
    return {"n": N, "relations": relations, "time": time}
