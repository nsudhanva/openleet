"""Number of Beautiful Partitions at |s| = 1000 with 80% non-prime digits (~160 valid cut points),
k = 150 and minLength = 2, so summing over every earlier position for each part end and part
count is ~6 * 10^7 steps."""

SEEDS = 2
N = 1000
K = 150
MIN = 2


def generate(rng):
    s = [rng.choice("2357") if rng.random() < 0.2 else rng.choice("14689") for _ in range(N)]
    s[0], s[-1] = rng.choice("2357"), rng.choice("14689")
    return {"s": "".join(s), "k": K, "minLength": MIN}
