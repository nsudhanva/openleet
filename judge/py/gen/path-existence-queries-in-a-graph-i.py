"""Path Existence Queries I at n = 10^5 sorted values and 10^5 queries, with a few gaps so the
graph splits into long components; BFS per query is quadratic."""

SEEDS = 2
N = 10**5
Q = 10**5


def generate(rng):
    max_diff = rng.choice([2, 10])
    nums, v = [], 0
    for _ in range(N):
        nums.append(v)
        if rng.random() < 0.001:
            v += max_diff + 1
        else:
            v += rng.randint(0, 1)
        v = min(v, 10**5)
    queries = [[rng.randrange(N), rng.randrange(N)] for _ in range(Q)]
    return {"n": N, "nums": nums, "maxDiff": max_diff, "queries": queries}
