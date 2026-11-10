"""Arithmetic Slices at n = 5000: all equal (~1.25 * 10^7 slices, the worst case for
enumerating them), long up-and-down progressions spanning the whole value range, or random
values with short runs."""

SEEDS = 3
N = 5000


def generate(rng):
    shape = rng.choice(["constant", "sweeps", "random"])
    if shape == "constant":
        nums = [rng.randint(-1000, 1000)] * N
    elif shape == "sweeps":
        up = list(range(-1000, 1001))
        nums = (up + up[-2::-1] + up[1:])[:N]
    else:
        nums = [rng.randint(-3, 3) for _ in range(N)]
    return {"nums": nums}
