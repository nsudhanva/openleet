"""Get the Maximum Score with two strictly increasing arrays of 10^5 values up to 10^7, sharing
few or many crossing points."""

SEEDS = 3
N = 10**5


def generate(rng):
    common_size = rng.choice([1, 100, 50_000])
    pool = rng.sample(range(1, 10**7 + 1), 2 * N - common_size)
    common = pool[:common_size]
    a = sorted(common + pool[common_size:N])
    b = sorted(common + pool[N:])
    return {"nums1": a, "nums2": b}
