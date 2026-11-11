"""Plates Between Candles on the maximum 10^5-character table with the maximum 10^5 queries each
spanning at least 96% of it, so counting plates per query does ~10^10 character visits."""

SEEDS = 2
N = 10**5
Q = 10**5


def generate(rng):
    s = "".join("|" if rng.random() < 0.1 else "*" for _ in range(N))
    queries = [[rng.randrange(N // 50), rng.randrange(N - N // 50, N)] for _ in range(Q)]
    return {"s": s, "queries": queries}
