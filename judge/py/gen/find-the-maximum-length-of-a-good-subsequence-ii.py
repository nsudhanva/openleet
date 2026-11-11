"""Find the Maximum Length of a Good Subsequence II at n = 5000 with k = 50 and 1500-3000
distinct values, so a DP over every earlier element or every distinct value is ~n^2 k."""

SEEDS = 2
N = 5000
K = 50


def generate(rng):
    kinds = rng.randint(1500, 3000)
    values = rng.sample(range(1, 10**9 + 1), kinds)
    return {"nums": [rng.choice(values) for _ in range(N)], "k": K}
