"""Maximum Distance Between a Pair of Values with two non-increasing arrays of 2 * 10^4: either
nums2 is nums1's line shifted right by a third to a half of n, so the answer is about that shift,
or the two lines track each other so every valid pair has j <= i + 1; trying every pair is
~2 * 10^8 checks."""

from _shapes import pick_shape

SEEDS = 2
N = 2 * 10**4
TOP = 10**5
STEP = 5


def generate(rng):
    shift = rng.randint(N // 3, N // 2) if pick_shape(rng) == 0 else 0
    nums1 = [TOP - STEP * i - rng.randint(0, 2) for i in range(N)]
    nums2 = [min(TOP, TOP - STEP * (j - shift) + rng.randint(0, STEP - 1)) for j in range(N)]
    for j in range(1, N):
        nums2[j] = min(nums2[j], nums2[j - 1])
    if not shift:
        nums2 = nums2[: N - rng.randrange(N // 100 + 1)]
    return {"nums1": nums1, "nums2": nums2}
