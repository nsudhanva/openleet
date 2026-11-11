"""Separate Squares II with 2 * 10^4 squares whose y-ranges all overlap (total area under 10^15), so
re-merging the active x-intervals at each of the 4 * 10^4 sweep events is ~10^4 work per event."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9
SIDE = (10**5, 2 * 10**5)


def generate(rng):
    width = rng.choice([LIMIT, 10**7])
    squares = []
    for _ in range(N):
        side = rng.randint(*SIDE)
        squares.append([rng.randint(0, width), rng.randint(0, SIDE[0]), side])
    return {"squares": squares}
