"""Number of Enclaves on a 120 by 120 grid: a random land band along the border, a ring of water,
and dense land inside it, so flood-filling from every land cell to look for the border costs the
square of the ~5,000-cell enclave."""

SEEDS = 2
N = 120
BAND = 10


def generate(rng):
    inner = rng.uniform(0.7, 0.8)
    grid = []
    for i in range(N):
        row = []
        for j in range(N):
            ring = min(i, j, N - 1 - i, N - 1 - j)
            if ring < BAND:
                row.append(int(rng.random() < 0.6))
            elif ring == BAND:
                row.append(0)
            else:
                row.append(int(rng.random() < inner))
        grid.append(row)
    return {"grid": grid}
