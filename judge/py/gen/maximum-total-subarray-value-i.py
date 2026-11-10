"""Maximum Total Subarray Value I at n = 5 * 10^4 with k up to 10^5 and values up to 10^9."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    nums = [rng.randint(0, 10**9) for _ in range(N)]
    return {"nums": nums, "k": rng.choice((10**5, rng.randint(1, 10**5)))}
