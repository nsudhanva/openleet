"""Minimum Number of Removals to Make Mountain Array at n = 1000 (the limit), so recomputing the
increasing run into and out of each candidate peak is cubic against the quadratic LIS tables."""

SEEDS = 2
N = 1000
LIMIT = 10**9


def generate(rng):
    nums = [rng.randint(1, LIMIT) for _ in range(N)]
    # A mountain must exist: a small value, then a larger one, then a small one.
    nums[0], nums[N // 2], nums[-1] = 1, LIMIT, 1
    return {"nums": nums}
