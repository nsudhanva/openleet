"""Path With Maximum Minimum Value on the maximum 100 x 100 grid: a top half of all-10^9 rows
with random low rows between them, one middle band, and a high bottom half, so trying each
threshold with a flood fill in either order does thousands of fills of ~10^4 cells."""

SEEDS = 2
M = 100
N = 100
H = 10**9


def generate(rng):
    grid = []
    for i in range(M // 2):
        if i == 0 or i % 2:
            grid.append([H] * N)
        else:
            grid.append([H] + [rng.randint(0, 4 * 10**8) for _ in range(N - 1)])
    grid.append([rng.randint(0, 5 * 10**8) for _ in range(N)])
    for _ in range(M // 2 + 1, M):
        grid.append([rng.randint(5 * 10**8 + 1, H - 1) for _ in range(N)])
    grid[-1][-1] = H
    return {"grid": grid}
