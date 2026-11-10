"""Divide Array in Sets of K Consecutive Numbers at n = 10^5: overlapping consecutive runs
shuffled together (answer true), or the same with one value nudged (answer false)."""

SEEDS = 3
N = 10**5


def generate(rng):
    k = rng.choice([1, 2, 5, 100, 1000])
    starts = rng.randint(1, 10**9 - 2000)
    spread = rng.choice([50, 10**5])
    nums = []
    for _ in range(N // k):
        s = starts + rng.randint(0, spread)
        nums.extend(range(s, s + k))
    while len(nums) < N and rng.random() < 0.5:
        nums.append(starts)
    if len(nums) % k == 0 and rng.random() < 0.5:
        i = rng.randrange(len(nums))
        nums[i] += 1
    rng.shuffle(nums)
    return {"nums": nums, "k": k}
