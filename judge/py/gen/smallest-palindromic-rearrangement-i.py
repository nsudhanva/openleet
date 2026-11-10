"""Smallest Palindromic Rearrangement I at length 10^5 (odd or even): a random palindrome, or
one built from a reverse-sorted half."""

SEEDS = 3


def generate(rng):
    n = rng.choice([10**5, 10**5 - 1])
    alphabet = rng.choice(["abcdefghijklmnopqrstuvwxyz", "ab", "z"])
    half = [rng.choice(alphabet) for _ in range(n // 2)]
    if rng.random() < 0.5:
        half.sort(reverse=True)
    middle = [rng.choice(alphabet)] if n % 2 else []
    return {"s": "".join(half + middle + half[::-1])}
