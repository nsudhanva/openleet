"""Longest Subsequence With Non-Zero XOR at n = 10^5: random values, an even count of one
repeated value (total XOR is zero), or all zeros."""

SEEDS = 3
N = 10**5
LIMIT = 10**9


def generate(rng):
    shape = rng.choice(["random", "cancel", "zeros"])
    if shape == "zeros":
        nums = [0] * N
    elif shape == "cancel":
        v = rng.randint(1, LIMIT)
        nums = [v] * N
        nums[rng.randrange(N)] = 0
        nums[rng.randrange(N)] = 0
    else:
        nums = [rng.randint(0, LIMIT) for _ in range(N - 1)]
        total = 0
        for v in nums:
            total ^= v
        # Make the whole array XOR to zero so the answer is n - 1 (or less).
        if total <= LIMIT:
            nums.append(total)
        else:
            nums.append(rng.randint(0, LIMIT))
        rng.shuffle(nums)
    return {"nums": nums}
