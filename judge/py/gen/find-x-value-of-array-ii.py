"""X-Value of Array II with n = 10^5, k up to 5, and 2 * 10^4 point updates each followed by a
query from a random start, so per-query rescans are quadratic."""

SEEDS = 3
N = 10**5
Q = 2 * 10**4


def generate(rng):
    k = rng.choice([5, 4, rng.randint(1, 5)])
    nums = [rng.randint(1, 10**9) for _ in range(N)]
    queries = []
    for _ in range(Q):
        start = rng.choice([0, rng.randrange(N)])
        queries.append([rng.randrange(N), rng.randint(1, 10**9), start, rng.randrange(k)])
    return {"nums": nums, "k": k, "queries": queries}
