"""Row With Maximum Ones on a 100 x 100 binary matrix, sometimes with ties on the maximum."""

SEEDS = 2


def generate(rng):
    p = rng.random()
    return {"mat": [[1 if rng.random() < p else 0 for _ in range(100)] for _ in range(100)]}
