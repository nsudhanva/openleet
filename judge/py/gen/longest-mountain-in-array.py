"""Longest Mountain at the maximum n = 10^4: a strict rise over 3/4 to 4/5 of the array that never
comes down (it ends in a plateau or at the array's end) next to one shorter mountain, or the
mirror image, so walking from every start (or end) is ~3 * 10^7 steps however early it stops."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
TOP = 10**4


def mountain(rng, base, size):
    """size strictly rising then falling values starting at base, the last one 0 if base is."""
    up = rng.randint(size // 4, size // 2)
    rise = [base, *sorted(rng.sample(range(base + 1, TOP), up))]
    fall = sorted(rng.sample(range(1, TOP), size - len(rise) - 1), reverse=True)
    return [*rise, TOP, *fall] if base else [*rise, TOP, *fall[:-1], 0]


def generate(rng):
    shape = pick_shape(rng)
    run = rng.randint(3 * N // 4, 4 * N // 5)
    if shape == 1:
        # The mountain falls to 0, then the rise climbs to the array's end.
        return {"arr": [*mountain(rng, 0, N - run), *sorted(rng.sample(range(1, TOP + 1), run))]}
    # The rise, a plateau, then the mountain from the plateau's level; reversed for shape 2, so a
    # long fall comes after the mountain instead.
    rise = sorted(rng.sample(range(run + 500), run))
    arr = [*rise, *mountain(rng, rise[-1], N - run)]
    return {"arr": arr[::-1] if shape == 2 else arr}
