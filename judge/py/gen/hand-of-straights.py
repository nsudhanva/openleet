"""Hand of Straights with 10^4 cards in descending order, split into overlapping runs of 2, 10 or
100 (one hand with its largest card raised, so it fails only at the end), so repeatedly taking
the minimum and removing cards from a list does ~10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
SIZES = (2, 10, 100)


def generate(rng):
    shape = pick_shape(rng)
    size = SIZES[shape]
    base = rng.randint(0, 10**9 - 4000)
    starts = [base + rng.randint(0, 3000) for _ in range(N // size)]
    hand = sorted((s + j for s in starts for j in range(size)), reverse=True)
    if shape == 1:
        hand[0] += 1
    return {"hand": hand, "groupSize": size}
