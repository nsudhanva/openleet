"""Unique Middle Element at the maximum odd n = 99, the middle value either unique or
repeated somewhere far from the middle."""

SEEDS = 2
N = 99


def generate(rng):
    nums = [rng.randint(1, 100) for _ in range(N)]
    mid = nums[N // 2]
    if rng.random() < 0.5:
        nums = [x if x != mid or i == N // 2 else (x % 100) + 1 for i, x in enumerate(nums)]
    else:
        nums[rng.choice([0, N - 1])] = mid
    return {"nums": nums}
