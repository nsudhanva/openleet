"""Longest Balanced Substring II at n = 2 * 10^4 over 'a', 'b', 'c', so extending every start with
running counts costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    # One seed skews toward 'a' so long balanced stretches are rare.
    weights = rng.choice(((1, 1, 1), (8, 1, 1)))
    return {"s": "".join(rng.choices("abc", weights=weights, k=N))}
