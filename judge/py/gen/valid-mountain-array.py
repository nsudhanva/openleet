"""Valid Mountain Array at n = 10^4: a real mountain, one with a plateau at the peak, or a
strictly increasing array with no descent."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4


def generate(rng):
    shape = pick_shape(rng)
    peak = rng.randint(1, N - 2)
    up = [*sorted(rng.sample(range(0, 10**4), peak)), 10**4]
    down = sorted(rng.sample(range(0, 10**4), N - peak - 1), reverse=True)
    arr = up + down
    if shape == 1:
        arr[peak + 1] = arr[peak]
    elif shape == 2:
        arr = sorted(rng.sample(range(0, 10**4 + 1), N))
    return {"arr": arr}
