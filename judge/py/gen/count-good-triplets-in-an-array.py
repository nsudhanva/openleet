"""Count Good Triplets in an Array at n = 5 * 10^4: nums2 is nums1 with a fraction of positions
shuffled, so many triplets agree and counting each middle's smaller neighbours by scanning costs
~1.25 * 10^9 steps."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    fraction = 0.1 if rng.random() < 0.5 else 0.6
    nums1 = list(range(N))
    rng.shuffle(nums1)
    nums2 = nums1[:]
    moved = rng.sample(range(N), int(N * fraction))
    vals = [nums2[i] for i in moved]
    rng.shuffle(vals)
    for i, v in zip(moved, vals, strict=True):
        nums2[i] = v
    return {"nums1": nums1, "nums2": nums2}
