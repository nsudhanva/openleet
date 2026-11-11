"""Count Subarrays With Majority Element II at n = 10^5 with the target making up 45% of the
array (the balance drifts down, so prefix sums insert near the front of a sorted list), so
recounting every subarray costs 5 * 10^9 steps."""

SEEDS = 2
N = 10**5
LIMIT = 10**6
SHARE = 0.45


def generate(rng):
    target = rng.randint(1, LIMIT)
    nums = [target if rng.random() < SHARE else rng.randint(1, LIMIT) for _ in range(N)]
    return {"nums": nums, "target": target}
