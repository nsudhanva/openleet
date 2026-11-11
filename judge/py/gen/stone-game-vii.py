"""Stone Game VII at n = 1,000, so recomputing each interval's remaining sum with a loop
instead of prefix sums is ~1.7 * 10^8 steps."""

SEEDS = 2
N = 1000
LIMIT = 1000


def generate(rng):
    if rng.random() < 0.5:
        return {"stones": [rng.randint(1, LIMIT) for _ in range(N)]}
    return {"stones": [rng.choice((1, LIMIT)) for _ in range(N)]}
