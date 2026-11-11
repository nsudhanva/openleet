"""Maximum Value of an Ordered Triplet II at n = 2 * 10^4, so pairing every middle index with
every later one costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"nums": [rng.randint(1, 10**6) for _ in range(N)]}
