"""Delete Columns to Make Sorted with 100 strings of length 1000: random letters, or mostly
sorted columns with a few violations near the bottom."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N, L = 100, 1000


def generate(rng):
    if rng.random() < 0.5:
        strs = [random_string(rng, ascii_lowercase, L) for _ in range(N)]
    else:
        cols = []
        for _ in range(L):
            col = sorted(rng.choice(ascii_lowercase) for _ in range(N))
            if rng.random() < 0.3:
                i = rng.randrange(N - 1)
                col[i], col[-1] = col[-1], col[i]
            cols.append(col)
        strs = ["".join(cols[c][r] for c in range(L)) for r in range(N)]
    return {"strs": strs}
