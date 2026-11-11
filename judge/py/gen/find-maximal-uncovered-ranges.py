"""Find Maximal Uncovered Ranges with n ~ 10^9 and 2 * 10^5 one-cell ranges, all separate and
listed in descending order, so splicing each one into sorted lists of merged blocks moves ~10^10
bytes, and scanning the blocks for each range or marking cells is ~10^10 steps."""

from itertools import accumulate

SEEDS = 2
N = 2 * 10**5


def generate(rng):
    # Gaps of 2 or 3 leave an uncovered cell between neighbours and keep the JSON near 3 MB.
    cells = list(accumulate(rng.randint(2, 3) for _ in range(N)))
    cells.reverse()
    return {"n": rng.randint(10**9 - 1000, 10**9), "ranges": [[c, c] for c in cells]}
