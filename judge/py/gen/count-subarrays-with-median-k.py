"""Count Subarrays With Median K at n = 2 * 10^4 (a permutation with k near the middle), so
extending every start costs 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    nums = list(range(1, N + 1))
    rng.shuffle(nums)
    return {"nums": nums, "k": rng.randint(N // 3, 2 * N // 3)}
