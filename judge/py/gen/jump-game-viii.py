"""Jump Game VIII at n = 3 * 10^4 with valley- or peak-shaped values, so from most indices the
next greater-or-equal or the next smaller value lies on the far slope and scanning forward for
it costs ~2 * 10^8 steps, even with suffix-max and suffix-min pruning."""

from _shapes import pick_shape

SEEDS = 3
N = 30000
LIMIT = 10**5


def generate(rng):
    # Shapes: a valley of distinct values, a peak of distinct values, a valley with repeats.
    shape = pick_shape(rng)
    if shape == 2:
        vals = sorted(rng.randint(0, LIMIT) for _ in range(N))
    else:
        vals = sorted(rng.sample(range(LIMIT + 1), N))
    down, up = sorted(vals[::2], reverse=True), vals[1::2]
    nums = up + down if shape == 1 else down + up
    costs = [rng.randint(0, LIMIT) for _ in range(N)]
    return {"nums": nums, "costs": costs}
