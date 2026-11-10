"""Maximize Distance Between Points on a Square with 1.5 * 10^4 unique boundary points and
k up to 25: a huge side, or side 3750 where every boundary lattice point is used."""

SEEDS = 3
COUNT = 15 * 10**3


def point(side, t):
    if t < side:
        return [0, t]
    if t < 2 * side:
        return [t - side, side]
    if t < 3 * side:
        return [side, 3 * side - t]
    return [4 * side - t, 0]


def generate(rng):
    shape = rng.choice(["huge", "full", "mid"])
    if shape == "full":
        side = COUNT // 4
        ts = list(range(4 * side))
        rng.shuffle(ts)
    else:
        side = 10**9 if shape == "huge" else rng.randint(4000, 10**5)
        ts = rng.sample(range(4 * side), COUNT)
    k = rng.choice([4, 25, rng.randint(4, 25)])
    return {"side": side, "points": [point(side, t) for t in ts], "k": k}
