"""Number of Different Subsequences GCDs at n = 5000 random values up to 2 * 10^4 (the maximum
always present), so taking the GCD of each candidate's multiples by a full scan of nums is
~10^8 steps against the harmonic sieve's ~2 * 10^5."""

SEEDS = 2
N = 5000
TOP = 2 * 10**4


def generate(rng):
    nums = [rng.randint(1, TOP) for _ in range(N - 1)] + [TOP]
    rng.shuffle(nums)
    return {"nums": nums}
