"""Intersection of Two Arrays II at the maximum length 1000 each with values in [0, 1000] and
many repeated values."""

SEEDS = 2


def generate(rng):
    hi = rng.choice([10, 1000])
    return {
        "nums1": [rng.randint(0, hi) for _ in range(1000)],
        "nums2": [rng.randint(0, hi) for _ in range(1000)],
    }
