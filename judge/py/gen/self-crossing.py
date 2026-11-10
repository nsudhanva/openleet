"""Self Crossing at n = 10^5: an ever-growing spiral (never crosses, full scan), a growing spiral
that turns inward and crosses at the very end, or random distances."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        return {"distance": [i + 1 for i in range(N)]}
    if shape == 1:
        d = [i + 1 for i in range(N - 1)]
        d.append(d[-2] + 1)  # reaches back to the segment two steps earlier
        return {"distance": d}
    return {"distance": [rng.randint(1, 10**5) for _ in range(N)]}
