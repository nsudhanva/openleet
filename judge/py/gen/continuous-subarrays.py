"""Continuous Subarrays at n = 10^5: long runs (n / 8 to n / 2) whose values stay within a
band of 3, with nearby bands, so extending every start until the band breaks costs ~10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums, base = [], rng.randint(10, 10**7)
    while len(nums) < N:
        run = rng.randint(N // 8, N // 2)
        nums += [base + rng.randint(0, 2) for _ in range(run)]
        base = min(max(base + rng.choice((-3, -2, -1, 1, 2, 3)), 1), 10**9 - 2)
    return {"nums": nums[:N]}
