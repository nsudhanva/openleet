"""Knight Probability on the largest board (25 x 25) with up to 100 moves, where unmemoized
recursion branches 8^k ways."""

SEEDS = 2


def generate(rng):
    n = 25
    return {
        "n": n,
        "k": rng.randint(90, 100),
        "row": rng.randrange(n),
        "column": rng.randrange(n),
    }
