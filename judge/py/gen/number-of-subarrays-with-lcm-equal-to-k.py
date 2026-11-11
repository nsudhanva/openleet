"""Number of Subarrays With LCM Equal to K at the maximum 1,000 values, all divisors of a k with
many divisors, so no subarray can be cut short and recomputing each subarray's LCM from scratch
costs ~1.7 * 10^8 steps."""

SEEDS = 2
N = 1000


def generate(rng):
    k = rng.choice((720, 840, 960))
    divisors = [d for d in range(1, k + 1) if k % d == 0]
    small = [d for d in divisors if d <= k // 8]
    nums = [rng.choice(small) for _ in range(N)]
    for i in rng.sample(range(N), N // 50):
        nums[i] = rng.choice(divisors)
    return {"nums": nums, "k": k}
