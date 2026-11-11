"""Find Maximum Area of a Triangle with 5 * 10^4 points: two lines of 10^4 points each plus 15,000
lines of two, so trying every pair on a line as the base is ~10^8 steps and scanning all points for
each line's farthest apex is ~7.5 * 10^8."""

SEEDS = 2
HEAVY = 10**4
LIGHT = 15 * 10**3
TOP = 10**6


def generate(rng):
    xs = rng.sample(range(1, TOP + 1), LIGHT + 2)
    coords = []
    for i, x in enumerate(xs):
        coords += [[x, y] for y in rng.sample(range(1, TOP + 1), HEAVY if i < 2 else 2)]
    if rng.random() < 0.5:
        coords = [[y, x] for x, y in coords]
    rng.shuffle(coords)
    return {"coords": coords}
