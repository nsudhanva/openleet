"""Majority Element II at n = 5 * 10^4: two values just above n / 3, one value just above
n / 3, or none (counts exactly n / 3 do not qualify)."""

SEEDS = 3
N = 5 * 10**4
LIMIT = 10**9


def generate(rng):
    shape = rng.choice([2, 1, 0])
    a, b = rng.sample(range(-LIMIT, LIMIT + 1), 2)
    third = N // 3
    if shape == 2:
        nums = [a] * (third + 1) + [b] * (third + 1)
    elif shape == 1:
        nums = [a] * (third + 1) + [b] * third
    else:
        nums = [a] * third + [b] * third
    while len(nums) < N:
        v = rng.randint(-LIMIT, LIMIT)
        if v not in (a, b):
            nums.append(v)
    rng.shuffle(nums)
    return {"nums": nums}
