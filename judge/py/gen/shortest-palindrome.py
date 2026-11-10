"""Shortest Palindrome at length 5 * 10^4: 'a...a' + 'b' + 'a...a' with the longer run first
(the quadratic worst case for prefix checks), or random over a small alphabet."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        k = rng.randint(N // 2, N - 2)
        return {"s": "a" * k + "b" + "a" * (N - 1 - k)}
    if shape == 1:
        return {"s": "a" * (N - 1) + "b"}
    return {"s": "".join(rng.choice("ab") for _ in range(N))}
