"""Total Waviness II over ranges spanning up to [1, 10^15], so only a digit DP is fast."""

from _shapes import pick_shape

SEEDS = 3
TOP = 10**15


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        return {"num1": 1, "num2": TOP}
    if shape == 1:
        return {"num1": rng.randint(1, 10**6), "num2": rng.randint(TOP // 2, TOP)}
    a, b = rng.randint(1, TOP), rng.randint(1, TOP)
    return {"num1": min(a, b), "num2": max(a, b)}
