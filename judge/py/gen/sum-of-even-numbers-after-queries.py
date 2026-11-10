"""Sum of Even Numbers After Queries at 10^4 numbers and 10^4 queries, punishing a full
re-sum after every query."""

SEEDS = 2
N = 10**4


def generate(rng):
    nums = [rng.randint(-(10**4), 10**4) for _ in range(N)]
    queries = [[rng.randint(-(10**4), 10**4), rng.randrange(N)] for _ in range(N)]
    return {"nums": nums, "queries": queries}
