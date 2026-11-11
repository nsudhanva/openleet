"""Minimum Distance Between Three Equal Elements II at n = 5 * 10^4: almost all values distinct,
a few wide triples and the tightest one near the end, so scanning ahead from each index for two
more copies is ~10^9 comparisons."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    nums = list(range(1, N + 1))
    rng.shuffle(nums)
    # A value at three random places for each of a few triples, then one tight triple near the end.
    for _ in range(5):
        i, j, k = rng.sample(range(N - 50), 3)
        nums[j] = nums[k] = nums[i]
    k = N - rng.randint(1, 20)
    i = k - rng.randint(2, 6)
    nums[i] = nums[rng.randint(i + 1, k - 1)] = nums[k]
    return {"nums": nums}
