"""Remove Duplicates from Sorted List at the maximum 300 nodes with long runs of equal values."""

SEEDS = 2


def generate(rng):
    span = rng.choice([5, 200])
    lo = rng.randint(-100, 100 - span)
    return {"head": sorted(rng.randint(lo, lo + span) for _ in range(300))}
