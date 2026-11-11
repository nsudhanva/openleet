"""Separate Squares II with 2 * 10^4 squares whose y-ranges all overlap (total area under 10^15)
and whose left edges lie in a range of 10^9, 10^7 or 3 * 10^5: the 4 * 10^4 sweep events each
touch ~10^4 active x-intervals when re-merged, and on the narrowest range each square spans
~10^4 compressed cells, so marking cells one by one is ~5 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
WIDTHS = (10**9, 10**7, 3 * 10**5)
SIDE = (10**5, 2 * 10**5)


def generate(rng):
    width = WIDTHS[pick_shape(rng)]
    squares = []
    for _ in range(N):
        side = rng.randint(*SIDE)
        squares.append([rng.randint(0, width), rng.randint(0, SIDE[0]), side])
    return {"squares": squares}
