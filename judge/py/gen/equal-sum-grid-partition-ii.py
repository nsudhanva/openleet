"""Equal Sum Grid Partition II on a 1 x 10^5 or 10^5 x 1 grid where no cut balances, even
after discounting an end cell of the heavier side, so trying each cut from scratch is ~10^10
steps."""

SEEDS = 2
N = 10**5


def balances(vals):
    total, prefix = sum(vals), 0
    for c in range(1, len(vals)):
        prefix += vals[c - 1]
        diff = 2 * prefix - total
        if diff == 0:
            return True
        # Only an end of a one-wide section can go without splitting it.
        if diff > 0 and diff in (vals[0], vals[c - 1]):
            return True
        if diff < 0 and -diff in (vals[c], vals[-1]):
            return True
    return False


def generate(rng):
    vals = [rng.randint(1, 10**5) for _ in range(N)]
    while balances(vals):
        vals[rng.randrange(N)] = rng.randint(1, 10**5)
    grid = [vals] if rng.random() < 0.5 else [[v] for v in vals]
    return {"grid": grid}
