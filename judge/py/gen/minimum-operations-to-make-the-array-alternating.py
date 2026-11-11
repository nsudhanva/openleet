"""Minimum Operations to Make the Array Alternating at n = 2 * 10^4 random values up to 10^5, so
each parity holds ~9000 distinct values and pairing every even-index value with every odd-index
value costs ~8 * 10^7 steps against keeping the top two of each."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    return {"nums": [rng.randint(1, LIMIT) for _ in range(N)]}
