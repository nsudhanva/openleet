"""Split Array With Same Average at the maximum n = 30, always false while every subset size
passes the divisibility test and the deviations from the mean mix signs, so a search over the
2^30 subsets, pruned by bounds or not, runs to the end."""

SEEDS = 2
N = 30
TOP = 10**4
M = 31  # A prime above N - 1.
SPREAD = 40


def generate(rng):
    # Deviations d = nums - mean: N - 1 of them are 1 mod M and the last makes the total 0, so
    # a proper subset of size j sums to j or j - N mod M, never 0: no split balances.
    while True:
        d = [1 + M * rng.randint(-SPREAD, SPREAD) for _ in range(N - 1)]
        d.append(-sum(d))
        if abs(d[-1]) <= M * SPREAD:
            break
    mean = rng.randint(-min(d), TOP - max(d))
    nums = [mean + x for x in d]
    rng.shuffle(nums)
    return {"nums": nums}
