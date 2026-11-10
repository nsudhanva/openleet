"""Meeting Rooms III at 10^5 meetings with unique starts: few rooms and long meetings so
delays pile up, or 100 rooms; per-meeting scans of every room and time are slow."""

SEEDS = 3
M = 10**5
TOP = 5 * 10**5


def generate(rng):
    n = rng.choice((1, 2, 100, rng.randint(1, 100)))
    starts = sorted(rng.sample(range(TOP), M))
    rng.shuffle(starts)
    longest = rng.choice((10, 1000, TOP))
    meetings = [[s, rng.randint(s + 1, min(TOP, s + longest))] for s in starts]
    return {"n": n, "meetings": meetings}
