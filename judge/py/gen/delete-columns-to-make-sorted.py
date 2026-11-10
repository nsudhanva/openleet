"""Delete Columns to Make Sorted with 100 strings of length 1000: random letters, or mostly
sorted columns with a few violations near the bottom."""

SEEDS = 2
N, L = 100, 1000
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    if rng.random() < 0.5:
        strs = ["".join(rng.choice(LETTERS) for _ in range(L)) for _ in range(N)]
    else:
        cols = []
        for _ in range(L):
            col = sorted(rng.choice(LETTERS) for _ in range(N))
            if rng.random() < 0.3:
                i = rng.randrange(N - 1)
                col[i], col[-1] = col[-1], col[i]
            cols.append(col)
        strs = ["".join(cols[c][r] for c in range(L)) for r in range(N)]
    return {"strs": strs}
