"""Number of Pairs Satisfying Inequality at 2 * 10^4 values per array, so checking every pair costs
2 * 10^8 comparisons."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**4


def generate(rng):
    return {
        "nums1": [rng.randint(-TOP, TOP) for _ in range(N)],
        "nums2": [rng.randint(-TOP, TOP) for _ in range(N)],
        "diff": rng.randint(-TOP, TOP),
    }
