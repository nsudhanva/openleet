"""Maximum Absolute Sum of Any Subarray at n = 10^5 with values in [-10^4, 10^4]: random, or
a long negative stretch so the best answer is a negative sum."""

SEEDS = 2
N = 10**5
LIMIT = 10**4


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    else:
        nums = [rng.randint(-LIMIT, LIMIT // 2) for _ in range(N)]
    return {"nums": nums}
