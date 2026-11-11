"""Regular Expression Matching at the maximum length 20: a pattern of nine or ten `x*` pairs that
cannot match, or alternating `x*` and `.*` pairs ending in a letter that is not in s (identical
neighbours cannot be merged), so backtracking without memo tries 10^6 to 10^7 ways to split the
run of x."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    x, y = rng.sample("abcdefghijklmnopqrstuvwxyz", 2)
    shape = pick_shape(rng)
    if shape == 0:
        return {"s": x * 19 + y, "p": (x + "*") * 10}
    if shape == 1:
        return {"s": x * 20, "p": (x + "*") * 9 + y}
    return {"s": x * 20, "p": (x + "*.*") * 4 + x + "*" + y}
