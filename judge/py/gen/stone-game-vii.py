"""Stone Game VII at n = 1,000 over 5 seeds, so recomputing each interval's remaining sum with a
loop instead of prefix sums is ~9 * 10^8 steps in all, past the 10 s cap on the limit."""

SEEDS = 5
N = 1000
LIMIT = 1000


def generate(rng):
    if rng.random() < 0.5:
        return {"stones": [rng.randint(1, LIMIT) for _ in range(N)]}
    return {"stones": [rng.choice((1, LIMIT)) for _ in range(N)]}
