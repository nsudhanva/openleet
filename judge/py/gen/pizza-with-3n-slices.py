"""Pizza With 3n Slices at the largest allowed 498 slices, so simulating every sequence of picks
explodes where the O(n^2) DP does ~1.6 * 10^5 steps."""

SEEDS = 2
N = 498


def generate(rng):
    return {"slices": [rng.randint(1, 1000) for _ in range(N)]}
