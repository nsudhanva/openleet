"""Maximum Binary String After Change at length 10^5 (the maximum) after a few leading ones:
either random bits or about 95% zeros, so applying the moves one at a time is ~10^9 swaps and
rebuilding the string per zero is ~5 * 10^9 copied characters."""

from _shapes import pick_shape

SEEDS = 2
N = 10**5


def generate(rng):
    ones = 0.5 if pick_shape(rng) == 0 else 0.05
    lead = rng.randint(0, 20)
    rest = "".join("1" if rng.random() < ones else "0" for _ in range(N - lead - 1))
    return {"binary": "1" * lead + "0" + rest}
