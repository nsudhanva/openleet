"""Set Matrix Zeroes on a 200 x 200 matrix of full 32-bit values with scattered zeros (some in
the first row and column)."""

SEEDS = 3


def generate(rng):
    m, n = 200, rng.choice([200, 199, 1])
    rate = rng.choice([0.0005, 0.01, 0.2])
    mat = [
        [0 if rng.random() < rate else rng.randint(-(2**31), 2**31 - 1) for _ in range(n)]
        for _ in range(m)
    ]
    if rng.random() < 0.5:
        mat[0][rng.randrange(n)] = 0
        mat[rng.randrange(m)][0] = 0
    return {"matrix": mat}
