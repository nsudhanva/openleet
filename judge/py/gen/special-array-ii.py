"""Special Array II at n = 10^5 with 5,000 queries spanning most of the array: parity
alternates except at one pair near the end, so scanning each query's range is ~4 * 10^8 steps."""

SEEDS = 2
N = 10**5
Q = 5000
LIMIT = 10**5


def generate(rng):
    first = rng.randrange(2)
    nums = [rng.randrange(1, LIMIT // 2) * 2 - ((i + first) % 2) for i in range(N)]
    # One same-parity pair close to the end: queries that cover it answer false, after a long scan.
    bad = N - rng.randint(10, 1000)
    nums[bad] = nums[bad - 1] + 2 if nums[bad - 1] + 2 <= LIMIT else nums[bad - 1] - 2
    queries = []
    for _ in range(Q):
        lo = rng.randrange(N // 10)
        hi = rng.randrange(N - N // 10, N)
        queries.append([lo, hi])
    return {"nums": nums, "queries": queries}
