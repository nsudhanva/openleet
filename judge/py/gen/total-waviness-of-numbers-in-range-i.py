"""Total Waviness I over ranges up to the full [1, 10^5]."""

SEEDS = 2
TOP = 10**5


def generate(rng):
    if rng.random() < 0.5:
        return {"num1": 1, "num2": TOP}
    a, b = rng.randint(1, TOP), rng.randint(1, TOP)
    return {"num1": min(a, b), "num2": max(a, b)}
