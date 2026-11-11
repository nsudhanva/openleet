"""Delete Columns to Make Sorted III with 100 strings of length 100, each sorted but for one or
three adjacent swaps, so nearly every pair of columns can be kept together and trying subsets of
columns is exponential."""

from string import ascii_lowercase

from _shapes import pick_shape

SEEDS = 2
N, L = 100, 100


def generate(rng):
    swaps = 1 if pick_shape(rng) == 0 else 3
    strs = []
    for _ in range(N):
        row = sorted(rng.choice(ascii_lowercase) for _ in range(L))
        # Swap only unequal neighbours, at distinct places, so the row really is unsorted.
        steps = [i for i in range(L - 1) if row[i] != row[i + 1]]
        for i in rng.sample(steps, min(swaps, len(steps))):
            row[i], row[i + 1] = row[i + 1], row[i]
        strs.append("".join(row))
    return {"strs": strs}
