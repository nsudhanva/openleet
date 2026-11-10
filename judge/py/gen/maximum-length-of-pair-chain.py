"""Maximum Length of Pair Chain with 1000 pairs in [-1000, 1000]: short pairs (long chain),
or long overlapping pairs."""

SEEDS = 2
N = 1000


def generate(rng):
    span = rng.choice([3, 500])
    pairs = []
    for _ in range(N):
        a = rng.randint(-1000, 999)
        b = rng.randint(a + 1, min(1000, a + span))
        pairs.append([a, b])
    return {"pairs": pairs}
