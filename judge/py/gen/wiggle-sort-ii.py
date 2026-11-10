"""Wiggle Sort II at n = 5 * 10^4 built from a real wiggle arrangement and shuffled (so an
answer exists), with the median value repeated about half the time, the case that breaks
naive interleaving."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    n = N if shape != 1 else N - 1
    mid = rng.randint(1, 5000)
    lows, highs = (n + 1) // 2, n // 2
    if shape == 2:
        low = [rng.randint(0, mid - 1) for _ in range(lows)]
        high = [rng.randint(mid, 5000) for _ in range(highs)]
    else:
        # Lows are mostly mid - 1 and highs mostly mid: heavy duplicates on both sides.
        low = [mid - 1 if rng.random() < 0.9 else rng.randint(0, mid - 1) for _ in range(lows)]
        high = [mid if rng.random() < 0.9 else rng.randint(mid, 5000) for _ in range(highs)]
    nums = low + high
    rng.shuffle(nums)
    return {"nums": nums}
