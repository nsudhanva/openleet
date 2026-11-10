"""Out of Boundary Paths on a 50 x 50 grid with maxMove = 50 from near the center, where
unmemoized recursion explodes and the count needs modulo."""

SEEDS = 2


def generate(rng):
    m = rng.randint(45, 50)
    n = rng.randint(45, 50)
    return {
        "m": m,
        "n": n,
        "maxMove": 50,
        "startRow": rng.randint(m // 2 - 5, m // 2 + 5),
        "startColumn": rng.randint(n // 2 - 5, n // 2 + 5),
    }
