"""Maximum Score of Spliced Array at n = 3 * 10^4, so trying every swapped range costs
~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    return {
        "nums1": [rng.randint(1, 10**4) for _ in range(N)],
        "nums2": [rng.randint(1, 10**4) for _ in range(N)],
    }
