"""Longest Non-decreasing Subarray From Two Arrays at n = 2 * 10^4 where one choice per index
always continues a long non-decreasing run, so running the DP from every start costs ~2 * 10^8
steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    base, x = [], 1
    for _ in range(N):
        x += rng.randint(0, 4 * 10**4)
        base.append(x)
    nums1, nums2 = [], []
    for b in base:
        noise = rng.randint(1, 10**9)
        if rng.random() < 0.5:
            nums1.append(b)
            nums2.append(noise)
        else:
            nums1.append(noise)
            nums2.append(b)
    # Two breaks, where both choices fall below everything before them.
    for i in rng.sample(range(N // 4, N), 2):
        nums1[i] = nums2[i] = 1
    return {"nums1": nums1, "nums2": nums2}
