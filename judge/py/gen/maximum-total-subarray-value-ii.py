"""Maximum Total Subarray Value II at n = 5 * 10^4 with k = 10^5 distinct subarrays to pick,
far too many to enumerate all n^2 / 2 subarrays; one seed has many equal values."""

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    top = rng.choice((10**9, 10))
    nums = [rng.randint(0, top) for _ in range(N)]
    return {"nums": nums, "k": rng.choice((10**5, rng.randint(1, 10**5)))}
