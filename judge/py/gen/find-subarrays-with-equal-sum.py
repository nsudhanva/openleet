"""Find Subarrays With Equal Sum at n = 1000: strictly increasing values (all pair sums distinct,
answer false) or a small value range (many equal sums)."""

SEEDS = 3
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        nums = sorted(rng.sample(range(-(10**9), 10**9 + 1), N))
        if rng.random() < 0.5:
            nums.reverse()
    else:
        nums = [rng.randint(-(10**9), 10**9) for _ in range(N)]
        i, j = sorted(rng.sample(range(N - 1), 2))
        if j > i + 1:
            nums[j], nums[j + 1] = nums[i], nums[i + 1]
    return {"nums": nums}
