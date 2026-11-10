"""Remove Boxes at the maximum 100 boxes with only a few colors interleaved, the worst case for
the O(n^4) DP and hopeless for brute force."""

SEEDS = 2


def generate(rng):
    colors = rng.choice([2, 3, 5])
    boxes = [rng.randint(1, colors) for _ in range(100)]
    return {"boxes": boxes}
