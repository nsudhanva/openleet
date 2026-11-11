"""Regular Expression Matching at the maximum length 20 with a pattern of nine or ten `x*` pairs
that cannot match, so backtracking without memo tries ~10^7 ways to split the run of x."""

SEEDS = 2


def generate(rng):
    x, y = rng.sample("abcdefghijklmnopqrstuvwxyz", 2)
    if rng.random() < 0.5:
        return {"s": x * 19 + y, "p": (x + "*") * 10}
    return {"s": x * 20, "p": (x + "*") * 9 + y}
