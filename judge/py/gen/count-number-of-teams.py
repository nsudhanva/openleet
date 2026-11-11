"""Count Number of Teams at n = 1000 distinct ratings, so trying every triple costs ~1.7 * 10^8
steps."""

SEEDS = 2
N = 1000
LIMIT = 10**5


def generate(rng):
    return {"rating": rng.sample(range(1, LIMIT + 1), N)}
