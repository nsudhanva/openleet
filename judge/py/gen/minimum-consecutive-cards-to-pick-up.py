"""Minimum Consecutive Cards to Pick Up at n = 10^5 distinct cards except that the first and last
match, so scanning forward from every card for its match is 5 * 10^9 steps."""

SEEDS = 2
N = 10**5
LIMIT = 10**6


def generate(rng):
    cards = rng.sample(range(LIMIT + 1), N - 1)
    return {"cards": [*cards, cards[0]]}
