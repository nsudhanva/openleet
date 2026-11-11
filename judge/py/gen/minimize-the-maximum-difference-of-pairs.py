"""Minimize the Maximum Difference of Pairs at n = 2 * 10^4 with p = 0.37 n, so the answer sits
mid-rank among the candidate differences and trying them in order from either end, each with a
greedy pass, is quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    return {"nums": [rng.randint(0, LIMIT) for _ in range(N)], "p": N * 37 // 100}
