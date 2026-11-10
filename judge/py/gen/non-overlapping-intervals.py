"""Non-overlapping Intervals at 10^5 intervals over [-5 * 10^4, 5 * 10^4]: short ones, or long
nested ones where most must be erased."""

SEEDS = 3
N = 10**5
LIMIT = 5 * 10**4


def generate(rng):
    span = rng.choice((3, 100, 2 * LIMIT))
    intervals = []
    for _ in range(N):
        a = rng.randint(-LIMIT, LIMIT - 1)
        intervals.append([a, rng.randint(a + 1, min(LIMIT, a + span))])
    return {"intervals": intervals}
