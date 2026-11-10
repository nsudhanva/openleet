"""Partition to K Equal Sum Subsets at 16 numbers, each value at most four times: built from k
groups of equal sum, or with one unit moved between two values (usually false), both hard for naive
backtracking."""

SEEDS = 3


def generate(rng):
    while True:
        k = rng.randint(2, 8)
        sizes = [2] * k
        for _ in range(16 - 2 * k):
            sizes[rng.randrange(k)] += 1
        target = rng.randint(2000, 9000)
        nums = []
        for size in sizes:
            cuts = sorted(rng.sample(range(1, target), size - 1))
            parts = [b - a for a, b in zip([0, *cuts], [*cuts, target], strict=False)]
            nums.extend(parts)
        if rng.random() < 0.4:
            i, j = rng.sample(range(16), 2)
            if nums[j] > 1:
                nums[i] += 1
                nums[j] -= 1
        counts = {}
        for v in nums:
            counts[v] = counts.get(v, 0) + 1
        if len(nums) == 16 and max(nums) <= 10**4 and max(counts.values()) <= 4:
            rng.shuffle(nums)
            return {"nums": nums, "k": k}
