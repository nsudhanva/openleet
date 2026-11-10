"""Maximum Difference Between Increasing Elements at n = 1000: strictly decreasing (answer
-1), or random values up to 10^9."""

SEEDS = 2
N = 1000


def generate(rng):
    nums = [rng.randint(1, 10**9) for _ in range(N)]
    if rng.random() < 0.5:
        nums = sorted(set(nums), reverse=True)
    return {"nums": nums}
