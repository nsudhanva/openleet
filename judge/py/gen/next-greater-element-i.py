"""Next Greater Element I at the maximum 1000 unique values in nums2 (nums1 a subset):
decreasing so most answers are -1 after a full scan, or random."""

SEEDS = 3
N = 1000


def generate(rng):
    nums2 = rng.sample(range(10**4 + 1), N)
    if rng.random() < 0.5:
        nums2.sort(reverse=True)
    nums1 = rng.sample(nums2, rng.choice((N, rng.randint(1, N))))
    return {"nums1": nums1, "nums2": nums2}
