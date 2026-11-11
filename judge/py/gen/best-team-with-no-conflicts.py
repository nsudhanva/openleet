"""Best Team With No Conflicts at n = 1000 (the maximum) with random scores and ages, so trying
every subset is hopeless and the quadratic DP does ~5 * 10^5 steps."""

SEEDS = 2
N = 1000


def generate(rng):
    span = rng.choice([1000, 30])
    scores = [rng.randint(1, 10**6) for _ in range(N)]
    return {"scores": scores, "ages": [rng.randint(1, span) for _ in range(N)]}
