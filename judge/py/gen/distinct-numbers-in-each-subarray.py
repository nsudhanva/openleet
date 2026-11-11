"""Distinct Numbers in Each Subarray at n = 10^5 with k near n / 2 and mostly distinct values,
so building a set per window is ~2.5 * 10^9 insertions."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = [rng.randint(1, 10**5) for _ in range(N)]
    k = rng.randint(N * 2 // 5, N * 3 // 5)
    return {"nums": nums, "k": k}
