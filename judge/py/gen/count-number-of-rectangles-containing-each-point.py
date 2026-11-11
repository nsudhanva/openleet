"""Count Number of Rectangles Containing Each Point at 3 * 10^4 rectangles and 3 * 10^4 points, so
checking every rectangle against every point costs 9 * 10^8 tests."""

SEEDS = 2
N = 3 * 10**4
LIMIT = 10**9
H = 100


def generate(rng):
    lengths = rng.sample(range(1, LIMIT + 1), N)
    rectangles = [[x, rng.randint(1, H)] for x in lengths]
    xs = rng.sample(range(1, LIMIT + 1), N)
    points = [[x, rng.randint(1, H)] for x in xs]
    return {"rectangles": rectangles, "points": points}
