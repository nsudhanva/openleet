"""Delete Columns to Make Sorted III with 100 strings of length 100, random or nearly
sorted rows, for the quadratic-in-columns DP at full size."""

SEEDS = 2
N, L = 100, 100
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    strs = []
    sorted_rows = rng.random() < 0.5
    for _ in range(N):
        row = [rng.choice(LETTERS) for _ in range(L)]
        if sorted_rows:
            row.sort()
            for _ in range(3):
                i, j = rng.randrange(L), rng.randrange(L)
                row[i], row[j] = row[j], row[i]
        strs.append("".join(row))
    return {"strs": strs}
