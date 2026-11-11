"""Minimum Suffix Flips at n = 10^5 over three seeds, nearly alternating (one run in twenty has
length 2), so ~95% of the positions need a flip and simulating each suffix flip costs ~10^10
character updates (~1.4 s even as 12 KB big-integer xors)."""

SEEDS = 3
N = 10**5


def generate(rng):
    out, bit = [], rng.randrange(2)
    while len(out) < N:
        out += [str(bit)] * (2 if rng.random() < 0.05 else 1)
        bit ^= 1
    return {"target": "".join(out[:N])}
