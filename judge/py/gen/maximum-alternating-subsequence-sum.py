"""Maximum Alternating Subsequence Sum at n = 10^5 with values up to 10^5 (sums exceed 32
bits), random or zigzag."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, 10**5) for _ in range(N)]
    else:
        nums = [
            rng.randint(9 * 10**4, 10**5) if i % 2 == 0 else rng.randint(1, 10) for i in range(N)
        ]
    return {"nums": nums}
