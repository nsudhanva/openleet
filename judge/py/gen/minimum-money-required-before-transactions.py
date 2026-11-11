"""Minimum Money Required Before Transactions with 2 * 10^4 transactions over the full range,
about half losing money: re-summing the other transactions' losses for each one is ~4 * 10^8
steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"transactions": [[rng.randint(0, 10**9), rng.randint(0, 10**9)] for _ in range(N)]}
