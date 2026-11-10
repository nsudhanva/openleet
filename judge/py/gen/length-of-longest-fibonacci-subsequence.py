"""Longest Fibonacci Subsequence at n = 1000 strictly increasing values: 1..1000 (dense, many
chains), or random values up to 10^9 hiding a long Fibonacci-like chain."""

SEEDS = 2
N = 1000
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.5:
        return {"arr": list(range(1, N + 1))}
    a, b = rng.randint(1, 50), rng.randint(51, 100)
    chain = {a, b}
    while a + b <= LIMIT:
        a, b = b, a + b
        chain.add(b)
    values = set(chain)
    while len(values) < N:
        values.add(rng.randint(1, LIMIT))
    return {"arr": sorted(values)}
