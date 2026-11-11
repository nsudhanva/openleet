"""Number of Pairs Satisfying Inequality at 10^5 values per array, so checking every pair costs
5 * 10^9 comparisons. The differences nums1[i] - nums2[i] fall from +10^4 to -10^4 in order, so
a sorted list kept with bisect.insort takes every new difference at the front and moves ~10^5
items per value; that is ~2.7 s a seed against ~0.3 s for the reference, and 7 seeds put it past
the time limit."""

SEEDS = 7
N = 10**5
TOP = 10**4


def generate(rng):
    diffs = sorted((rng.randint(-TOP, TOP) for _ in range(N)), reverse=True)
    nums2 = [rng.randint(max(-TOP, -TOP - d), min(TOP, TOP - d)) for d in diffs]
    nums1 = [b + d for b, d in zip(nums2, diffs, strict=True)]
    return {"nums1": nums1, "nums2": nums2, "diff": rng.randint(-TOP, TOP)}
