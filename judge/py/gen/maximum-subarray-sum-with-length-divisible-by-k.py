"""Maximum Subarray Sum With Length Divisible by K: n = 8 * 10^4 with k near n / 2 on seed 0, so
an O(n k) block-sum DP costs ~3 * 10^9 steps, and n = 3 * 10^4 with k = 1 or 2 on seed 1, so
checking every allowed length at every start costs ~2-4.5 * 10^8."""

SEEDS = 2
N = 3 * 10**4
BIG = 8 * 10**4


def generate(rng):
    # The first draw is 0.84 for seed 0 and 0.13 for seed 1, so the seeds take both branches.
    if rng.random() < 0.5:
        n, k = N, rng.randint(1, 2)
    else:
        n = BIG
        k = n // 2 + rng.randint(-(n // 80), n // 80)
    return {"nums": [rng.randint(-(10**9), 10**9) for _ in range(n)], "k": k}
