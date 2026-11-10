"""Two Non-Overlapping Square Submatrices on a 500 x 500 binary matrix: nearly all ones (big
squares everywhere), random cells, or a long thin shape."""

SEEDS = 3


def generate(rng):
    shape = rng.choice(["ones", "random", "thin"])
    if shape == "thin":
        m, n = rng.choice([(500, 3), (2, 500)])
        p = 0.95
    else:
        m = n = 500
        p = 0.999 if shape == "ones" else 0.6
    return {"mat": [[1 if rng.random() < p else 0 for _ in range(n)] for _ in range(m)]}
