"""Find Maximal Uncovered Ranges with n ~ 10^9 and 6 * 10^4 one-cell ranges, all separate and listed
in descending order, so merging each one into the result by scanning it (or splicing it into sorted
lists) is ~2 * 10^9 steps (and marking cells needs 10^9)."""

SEEDS = 2
N = 6 * 10**4
SPAN = 10**5


def generate(rng):
    # Even cells below 2 * SPAN keep the JSON under 1 MB and leave a gap between neighbours.
    cells = sorted((2 * v for v in rng.sample(range(SPAN), N)), reverse=True)
    return {"n": rng.randint(10**9 - 1000, 10**9), "ranges": [[c, c] for c in cells]}
