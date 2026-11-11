"""Count Subarrays With Fixed Bounds at n = 2 * 10^4 with every value inside [minK, maxK], so
extending every start to the end costs 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**6


def generate(rng):
    min_k = rng.randint(1, LIMIT // 2)
    max_k = rng.randint(min_k, LIMIT)
    nums = [rng.randint(min_k, max_k) for _ in range(N)]
    for _ in range(3):
        nums[rng.randrange(N)] = min_k
        nums[rng.randrange(N)] = max_k
    return {"nums": nums, "minK": min_k, "maxK": max_k}
