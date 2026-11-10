"""Binary Search at n = 10^4 distinct sorted values: targets at either end, absent, or random."""

SEEDS = 3
N = 10**4


def generate(rng):
    nums = sorted(rng.sample(range(-9999, 10**4), N))
    r = rng.random()
    if r < 0.25:
        target = nums[0]
    elif r < 0.5:
        target = nums[-1]
    elif r < 0.75:
        present = set(nums)
        missing = [v for v in range(-9999, 10**4) if v not in present]
        target = rng.choice(missing)
    else:
        target = rng.choice(nums)
    return {"nums": nums, "target": target}
