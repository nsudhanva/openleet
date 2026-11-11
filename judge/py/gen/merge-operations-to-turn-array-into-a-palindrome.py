"""Merge Operations to Turn Array into a Palindrome at the maximum n = 10^5. Seed 0: small values
closed by their total, so every merge is at the front; seed 1: mirrored blocks split into different
parts on each side, so merges happen at both ends. Merging inside a list costs ~10^9 moves."""

SEEDS = 2
N = 10**5


def generate(rng):
    # The first draw is 0.84 for seed 0 and 0.13 for seed 1, so the seeds take both shapes.
    if rng.random() >= 0.5:
        nums = [rng.randint(1, 10) for _ in range(N - 1)]
        return {"nums": [*nums, sum(nums)]}
    # Equal block sums at mirrored places, each cut into 1-8 parts on the left and on the right.
    left, right = [], []
    while len(left) + len(right) < N - 17:
        parts = [rng.randint(1, 10) for _ in range(rng.randint(1, 8))]
        total = sum(parts)
        pieces = min(rng.randint(1, 8), total)
        cuts = sorted(rng.sample(range(1, total), pieces - 1))
        left += parts
        right += [b - a for a, b in zip([0, *cuts], [*cuts, total], strict=True)]
    return {"nums": [*left, rng.randint(1, 10), *reversed(right)]}
