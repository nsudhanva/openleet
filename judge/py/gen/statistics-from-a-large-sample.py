"""Statistics from a Large Sample with every count near 4 * 10^6 (sum close to 10^9) and one
unique mode, so expanding the sample into a list is ~10^9 steps."""

SEEDS = 2
TOTAL = 10**9


def generate(rng):
    # The first draw picks the shape, so seeds 0 and 1 take different branches.
    sparse = rng.random() < 0.5
    count = [rng.randint(3 * 10**6, 39 * 10**5) for _ in range(256)]
    count[rng.randrange(256)] = 39 * 10**5 + rng.randint(1, 10**5)
    if sparse:
        for k in rng.sample(range(256), 40):
            if count[k] < 39 * 10**5:
                count[k] = 0
    return {"count": count}
