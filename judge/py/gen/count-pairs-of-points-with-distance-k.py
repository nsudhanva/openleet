"""Count Pairs of Points With Distance K at 5 * 10^4 distinct points packed into a 224 x 224 box
(many pairs at distance k) with k <= 12, so testing every pair, even of distinct points only,
costs 1.25 * 10^9 checks."""

SEEDS = 2
N = 5 * 10**4
BOX = 224


def generate(rng):
    cells = rng.sample(range(BOX * BOX), N)
    coordinates = [[c // BOX, c % BOX] for c in cells]
    return {"coordinates": coordinates, "k": rng.randint(4, 12)}
