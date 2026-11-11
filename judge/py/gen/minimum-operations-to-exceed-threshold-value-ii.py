"""Minimum Operations to Exceed Threshold Value II at n = 2 * 10^4 with k = 10^9 and values spread
below it, so ~10^4 operations are needed and finding the two smallest by a scan each time is
quadratic against a heap."""

SEEDS = 2
N = 2 * 10**4
K = 10**9


def generate(rng):
    nums = [rng.randint(1, K) for _ in range(N - 1)]
    # One element already at k makes an answer certain: any small element pairs up to reach it.
    nums.insert(rng.randrange(N), K)
    return {"nums": nums, "k": K}
