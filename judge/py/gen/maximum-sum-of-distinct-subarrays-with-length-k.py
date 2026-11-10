"""Maximum Sum of Distinct Subarrays With Length K at n = 10^5 with large k: a permutation
(every window distinct) or values from a narrow range (repeats everywhere)."""

SEEDS = 3
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = list(range(1, N + 1))
        rng.shuffle(nums)
        k = rng.randint(N // 4, N)
    else:
        top = rng.randint(1000, 5000)
        nums = [rng.randint(1, top) for _ in range(N)]
        k = rng.randint(10, 60)
    return {"nums": nums, "k": k}
