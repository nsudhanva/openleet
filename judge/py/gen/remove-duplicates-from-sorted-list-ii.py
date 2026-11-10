"""Remove Duplicates from Sorted List II at the maximum 300 nodes: duplicate runs mixed with
singletons, including runs at both ends."""

SEEDS = 2


def generate(rng):
    span = rng.choice([30, 200])
    lo = rng.randint(-100, 100 - span)
    return {"head": sorted(rng.randint(lo, lo + span) for _ in range(300))}
