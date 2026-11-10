"""Interval List Intersections with 1000 disjoint sorted intervals per list over [0, 10^9], one
list sometimes made of a few huge intervals covering many of the other's."""

SEEDS = 3
N = 1000


def intervals(rng, count, hi):
    points = sorted(rng.sample(range(hi + 1), 2 * count))
    return [[points[2 * i], points[2 * i + 1]] for i in range(count)]


def generate(rng):
    hi = rng.choice([5000, 10**9])
    first = intervals(rng, N, hi)
    second = intervals(rng, rng.choice([N, 3]), hi)
    if rng.random() < 0.5:
        first, second = second, first
    return {"firstList": first, "secondList": second}
