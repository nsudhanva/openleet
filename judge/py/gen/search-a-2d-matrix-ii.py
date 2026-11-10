"""Search a 2D Matrix II on a 300 x 300 matrix sorted along rows and columns, target present,
absent, or in the far corner."""

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    m, n = 300, 300
    step = rng.choice([3, 1000, 10**6])
    mat = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            base = -(10**9)
            if i:
                base = max(base, mat[i - 1][j])
            if j:
                base = max(base, mat[i][j - 1])
            mat[i][j] = base + rng.randint(0, step)
    if shape == 0:
        target = mat[rng.randrange(m)][rng.randrange(n)]
    elif shape == 1:
        target = mat[m - 1][0] if rng.random() < 0.5 else mat[0][n - 1]
    else:
        target = rng.randint(mat[0][0], mat[m - 1][n - 1])
    return {"matrix": mat, "target": target}
