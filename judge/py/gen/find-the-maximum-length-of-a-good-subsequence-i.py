"""Find the Maximum Length of a Good Subsequence I at n = 100 over a few values with k = 10:
trying every subsequence is 2^100, while the O(n^2 k) DP is 10^5 steps."""

SEEDS = 2
N = 100
K = 10


def generate(rng):
    kinds = rng.randint(3, 8)
    values = rng.sample(range(1, 10**9 + 1), kinds)
    return {"nums": [rng.choice(values) for _ in range(N)], "k": K}
