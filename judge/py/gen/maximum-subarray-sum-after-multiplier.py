"""Maximum Subarray Sum After Multiplier at n = 3 * 10^4, so trying every operated range costs
~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    nums = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    return {"nums": nums, "k": rng.randint(2, 10**5)}
