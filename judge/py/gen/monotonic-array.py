"""Monotonic Array at n = 10^5: a non-decreasing or non-increasing run, sometimes broken by a
single violation near the end."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = sorted(rng.randint(-(10**5), 10**5) for _ in range(N))
    if rng.random() < 0.5:
        nums.reverse()
    if rng.random() < 0.6:
        i = rng.randint(N - 100, N - 2)
        nums[i], nums[i + 1] = nums[i + 1], nums[i]
        if nums[i] == nums[i + 1]:
            nums[i + 1] = -(10**5) if nums[0] <= nums[-1] else 10**5
    return {"nums": nums}
