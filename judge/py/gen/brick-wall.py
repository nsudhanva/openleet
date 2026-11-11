"""Brick Wall at the maximum 2 * 10^4 bricks: 10^4 two-brick rows of a huge width with (nearly)
all-distinct cuts, so counting the rows at each distinct edge separately costs ~10^8 row
checks."""

SEEDS = 2
ROWS = 10**4


def generate(rng):
    width = rng.randint(10**9, 2**31 - 1)
    cuts = rng.sample(range(1, width), ROWS)
    if rng.random() < 0.5:
        # A few popular edges, so the best line is not just any edge.
        popular = cuts[:5]
        cuts = [rng.choice(popular) if rng.random() < 0.05 else c for c in cuts]
    return {"wall": [[c, width - c] for c in cuts]}
