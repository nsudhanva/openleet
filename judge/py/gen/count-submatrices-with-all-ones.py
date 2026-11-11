"""Count Submatrices With All Ones on a 150 x 150 matrix that is almost all ones, so growing
every submatrix from every top-left corner costs ~1.3 * 10^8 steps."""

SEEDS = 2
M = N = 150


def generate(rng):
    zeros = rng.randint(0, 20)
    mat = [[1] * N for _ in range(M)]
    for _ in range(zeros):
        mat[rng.randrange(M)][rng.randrange(N)] = 0
    return {"mat": mat}
