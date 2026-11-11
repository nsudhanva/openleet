"""Maximum Strength of K Disjoint Subarrays at n = 10^4 and k = 5, so choosing each subarray's
start by a scan over earlier positions costs ~2.5 * 10^8 steps."""

SEEDS = 2
N = 10**4
K = 5


def generate(rng):
    return {"nums": [rng.randint(-(10**9), 10**9) for _ in range(N)], "k": K}
