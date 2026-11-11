"""Minimum Score Triangulation of Polygon with 20 vertices, so splitting on every apex by plain
recursion (~3^n calls) never finishes while the interval DP is ~1300 steps."""

SEEDS = 2
N = 20


def generate(rng):
    return {"values": [rng.randint(1, 100) for _ in range(N)]}
