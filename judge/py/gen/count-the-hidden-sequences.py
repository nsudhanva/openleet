"""Count the Hidden Sequences at n = 2000 small differences and the widest bounds, so trying
each of the ~2 * 10^5 starting values against the whole sequence costs ~4 * 10^8 steps."""

SEEDS = 2
N = 2000
LIMIT = 10**5


def generate(rng):
    differences = [rng.randint(-5, 5) for _ in range(N)]
    lower = -LIMIT + rng.randint(0, LIMIT // 1000)
    upper = LIMIT - rng.randint(0, LIMIT // 1000)
    return {"differences": differences, "lower": lower, "upper": upper}
