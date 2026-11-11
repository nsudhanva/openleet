"""Subarray With Elements Greater Than Varying Threshold at n = 2 * 10^4 where nums[i] is at
most threshold / (i + 1) (a falling curve, sometimes with dips), so no subarray qualifies and
extending every start to the end is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    # The first draw picks the shape, so seeds 0 and 1 take different branches.
    dips = rng.random() < 0.5
    threshold = rng.randint(LIMIT // 2, LIMIT)
    nums = [threshold // (i + 1) for i in range(N)]
    if dips:
        nums = [max(1, v - rng.randrange(v // 4 + 1)) for v in nums]
    return {"nums": nums, "threshold": threshold}
