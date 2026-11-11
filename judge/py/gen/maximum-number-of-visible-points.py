"""Maximum Number of Visible Points with 2 * 10^4 points on the 101 x 101 grid, so counting the
points in the view from every starting angle is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    points = [[rng.randint(0, 100), rng.randint(0, 100)] for _ in range(N)]
    return {"points": points, "angle": rng.randint(30, 120), "location": rng.choice(points)[:]}
