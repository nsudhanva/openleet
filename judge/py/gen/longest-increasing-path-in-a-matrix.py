"""Longest Increasing Path on a 200 x 200 matrix: a snake path that climbs through all 40,000
cells (deep DFS, exponential without memoization), or small random values."""

SEEDS = 2
N = 200


def generate(rng):
    if rng.random() < 0.5:
        matrix = [[0] * N for _ in range(N)]
        step = 0
        for r in range(N):
            cols = range(N) if r % 2 == 0 else range(N - 1, -1, -1)
            for c in cols:
                matrix[r][c] = step
                step += 1
        if rng.random() < 0.5:
            matrix = [[N * N - 1 - v for v in row] for row in matrix]
    else:
        matrix = [[rng.randint(0, 20) for _ in range(N)] for _ in range(N)]
    return {"matrix": matrix}
