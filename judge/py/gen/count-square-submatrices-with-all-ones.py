"""Count Square Submatrices with All Ones on a 300 x 300 matrix: all ones (every square counts,
punishing per-square checks), or dense random ones."""

SEEDS = 2
SIZE = 300


def generate(rng):
    if rng.random() < 0.5:
        matrix = [[1] * SIZE for _ in range(SIZE)]
    else:
        matrix = [[1 if rng.random() < 0.9 else 0 for _ in range(SIZE)] for _ in range(SIZE)]
    return {"matrix": matrix}
