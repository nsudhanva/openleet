"""Detect Squares with 3000 calls on one lattice: either 1000 adds on a 5 x 5 lattice (about 40
copies of each point) and 2000 counts, so scanning the stored points for the other corners of
every diagonal is ~8 * 10^8 steps, or every point of a 42 x 42 lattice added once and 1236
counts near its middle, so pairing up the distinct points for every count is ~10^9 steps."""

from _shapes import pick_shape

SEEDS = 3
CALLS = 3000
SPARSE_ADDS = 1000
SIDE = 5
DENSE = 42


def generate(rng):
    dense = pick_shape(rng) == 1
    side = DENSE if dense else SIDE
    step = rng.randint(1, 1000 // (side - 1))
    x0 = rng.randint(0, 1000 - step * (side - 1))
    y0 = rng.randint(0, 1000 - step * (side - 1))

    def lattice(lo=0, hi=side):
        return [x0 + step * rng.randrange(lo, hi), y0 + step * rng.randrange(lo, hi)]

    if dense:
        cells = rng.sample(range(side * side), side * side)
        added = [[x0 + step * (c // side), y0 + step * (c % side)] for c in cells]
        # Counts near the middle, where the most stored points share a diagonal with them.
        lo, hi = side // 4, side - side // 4
    else:
        added = [lattice() for _ in range(SPARSE_ADDS)]
        lo, hi = 0, side
    ops, args = ["DetectSquares"], [[]]
    for point in added:
        ops.append("add")
        args.append([point])
    while len(ops) <= CALLS:
        ops.append("count")
        if rng.random() < 0.9:
            args.append([lattice(lo, hi)])
        else:
            args.append([[rng.randint(0, 1000), rng.randint(0, 1000)]])
    return {"ops": ops, "args": args}
