"""XOR Queries of a Subarray at 2 * 10^4 values and 2 * 10^4 queries, each spanning most of
the array, so XOR-ing every range is ~3 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    arr = [rng.randint(1, 10**9) for _ in range(N)]
    queries = []
    for _ in range(N):
        left = rng.randrange(N // 10)
        queries.append([left, rng.randrange(N - N // 10, N)])
    return {"arr": arr, "queries": queries}
