"""Minimum Operations to Make Array Elements Zero with 200 queries spanning 5 * 10^4 to 10^5
values each, so counting the divisions by 4 for every value in every range costs ~2 * 10^8 steps
against summing over the powers of four."""

SEEDS = 2
Q = 200
SHORT = 5 * 10**4
LONG = 10**5
LIMIT = 10**9


def generate(rng):
    queries = []
    for _ in range(Q):
        length = rng.randint(SHORT, LONG)
        left = rng.randint(1, LIMIT - length)
        queries.append([left, left + length])
    return {"queries": queries}
