"""Ones and Zeroes at 600 strings with m = n = 100, the full O(len * m * n) knapsack; short
strings so many fit."""

SEEDS = 2


def generate(rng):
    maxlen = rng.choice([6, 100])
    strs = []
    for _ in range(600):
        length = rng.randint(1, maxlen)
        p = rng.random()
        strs.append("".join("1" if rng.random() < p else "0" for _ in range(length)))
    return {"strs": strs, "m": rng.randint(90, 100), "n": rng.randint(90, 100)}
