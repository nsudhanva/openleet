"""Separate Squares I with 10^4 squares of side up to 10^4 (total area under 10^12), so recomputing
the area below each of the 2 * 10^4 candidate lines is ~10^8 steps."""

SEEDS = 2
N = 10**4
SIDE = 10**4
LIMIT = 10**9


def generate(rng):
    span = rng.choice([LIMIT - SIDE, 10**5])
    squares = []
    for _ in range(N):
        side = rng.randint(1, SIDE)
        squares.append([rng.randint(0, LIMIT), rng.randint(0, span), side])
    return {"squares": squares}
