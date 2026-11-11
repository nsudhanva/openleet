"""Minimum Suffix Flips at n = 10^5 with runs of length 1 or 2, so ~2/3 of the positions need a
flip and simulating each suffix flip costs ~3 * 10^9 character updates."""

SEEDS = 2
N = 10**5


def generate(rng):
    out, bit = [], rng.randrange(2)
    while len(out) < N:
        out += [str(bit)] * rng.choice((1, 1, 2))
        bit ^= 1
    return {"target": "".join(out[:N])}
