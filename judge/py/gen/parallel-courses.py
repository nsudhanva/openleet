"""Parallel Courses at the maximum 5000 courses and 5000 relations: one shuffled chain through
every course plus a shortcut, so 5000 semesters each rescanning all relations do ~2.5 * 10^7
steps."""

SEEDS = 2
N = 5000


def generate(rng):
    order = rng.sample(range(1, N + 1), N)
    relations = [[order[i], order[i + 1]] for i in range(N - 1)]
    a = rng.randrange(N - 2)
    relations.append([order[a], order[rng.randrange(a + 2, N)]])
    rng.shuffle(relations)
    return {"n": N, "relations": relations}
