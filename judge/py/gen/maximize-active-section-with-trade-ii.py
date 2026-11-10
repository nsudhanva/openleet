"""Maximize Active Section with Trade II with s and the query list both at 10^5, mostly long
ranges, so answering each query by scanning its substring is quadratic."""

from _shapes import random_string

SEEDS = 2
N = 10**5
Q = 10**5


def generate(rng):
    if rng.random() < 0.5:
        s = random_string(rng, "01", N)
    else:
        parts, total, bit = [], 0, rng.choice("01")
        while total < N:
            length = min(N - total, rng.randint(1, 50))
            parts.append(bit * length)
            total += length
            bit = "1" if bit == "0" else "0"
        s = "".join(parts)
    queries = []
    for _ in range(Q):
        if rng.random() < 0.8:
            left = rng.randint(0, N // 10)
            right = rng.randint(N - N // 10, N - 1)
        else:
            left = rng.randrange(N)
            right = rng.randint(left, N - 1)
        queries.append([left, right])
    return {"s": s, "queries": queries}
