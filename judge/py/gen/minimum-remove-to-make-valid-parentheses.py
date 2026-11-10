"""Minimum Remove to Make Valid Parentheses at length 10^5: random brackets and letters, or
deeply nested '(' runs with stray ')', so repeated string rebuilding is quadratic."""

from _shapes import random_string

SEEDS = 3
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        return {"s": random_string(rng, "()()abc", N)}
    open_run = rng.randint(N // 4, N // 2)
    rest = N - open_run
    tail = [rng.choice(")))a") for _ in range(rest)]
    return {"s": "(" * open_run + "".join(tail)}
