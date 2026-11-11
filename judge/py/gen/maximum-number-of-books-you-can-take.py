"""Maximum Number of Books You Can Take with 3 * 10^4 shelves: a slow rise, then a flat half at the
cap where books[i] - i keeps falling, so walking left from every right end is quadratic."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    slope = rng.choice((1, 2))
    flat = N // 2
    head = [min(10**5, slope * i + rng.randint(0, 50)) for i in range(N - flat)]
    return {"books": head + [10**5 - rng.randint(0, 3) for _ in range(flat)]}
