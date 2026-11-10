"""Target Sum at the maximum 20 numbers with the sum near 1000 (and zeros that double the
count), so plain 2^20 recursion is slow next to the subset-sum DP."""

SEEDS = 3
N = 20


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        nums = [rng.randint(0, 3) for _ in range(N)]
    elif shape == 1:
        nums = [0] * 5 + [rng.randint(1, 60) for _ in range(N - 5)]
    else:
        nums = [rng.randint(0, 100) for _ in range(N)]
    while sum(nums) > 1000:
        i = max(range(N), key=lambda j: nums[j])
        nums[i] -= 1
    rng.shuffle(nums)
    total = sum(nums)
    target = rng.randint(-total, total) if rng.random() < 0.7 else rng.randint(-1000, 1000)
    return {"nums": nums, "target": target}
