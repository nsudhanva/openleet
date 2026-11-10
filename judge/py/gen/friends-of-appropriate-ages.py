"""Friends of Appropriate Ages with 2 * 10^4 people, ages spread over 1..120 or bunched."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    lo = rng.choice([1, 90])
    return {"ages": [rng.randint(lo, 120) for _ in range(N)]}
