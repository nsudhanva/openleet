"""Find the Number of Good Pairs II with 10^5 values in nums1, each k times a number in the top
half of the range, and 10^4 in nums2, so testing every pair or every divisor up to the square
root is ~10^9 or ~10^8 steps against counting multiples."""

SEEDS = 2
N = 10**5
M = 10**4
TOP = 10**6


def generate(rng):
    k = rng.randint(1, 2)
    nums1 = [k * rng.randint(TOP // (2 * k), TOP // k) for _ in range(N)]
    nums2 = [rng.randint(1, TOP // k) for _ in range(M)]
    return {"nums1": nums1, "nums2": nums2, "k": k}
