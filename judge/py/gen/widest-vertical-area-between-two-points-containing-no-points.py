"""Widest Vertical Area at 10^5 points with random coordinates. Two seeds list the points from
right to left, so building the sorted x list with bisect.insort moves ~10^5 items per point; the
third is shuffled. Finding each point's next x to the right by scanning is ~10^10 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5
TOP = 10**9


def generate(rng):
    xs = [rng.randint(0, TOP) for _ in range(N)]
    if pick_shape(rng) != 1:
        xs.sort(reverse=True)
    return {"points": [[x, rng.randint(0, TOP)] for x in xs]}
