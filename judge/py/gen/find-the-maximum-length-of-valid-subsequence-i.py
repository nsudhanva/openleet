"""Find the Maximum Length of Valid Subsequence I at n = 5 * 10^4, so a DP over every earlier
element is ~10^9 steps against the O(n) parity scan."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    odd = rng.choice((0.5, 0.1))
    nums = [
        rng.randrange(1, 10**7, 2) if rng.random() < odd else rng.randrange(2, 10**7 + 1, 2)
        for _ in range(N)
    ]
    return {"nums": nums}
