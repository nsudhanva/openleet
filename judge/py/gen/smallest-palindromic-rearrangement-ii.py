"""Smallest Palindromic Rearrangement II at length 10^4: many distinct letters (the permutation
count overflows any fixed-width integer) with k up to 10^6, or few letters so k may exceed the
count."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    n = rng.choice([10**4, 10**4 - 1])
    if shape == 0:
        half = [rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n // 2)]
    elif shape == 1:
        # Two letters, one of them rare: only C(5000, few) permutations.
        half = ["a"] * (n // 2)
        for i in rng.sample(range(n // 2), 3):
            half[i] = "b"
    else:
        half = ["a"] * (n // 2 - 1) + ["b"]
    rng.shuffle(half)
    middle = [rng.choice("abc")] if n % 2 else []
    k = rng.choice([10**6, rng.randint(1, 10**6)])
    return {"s": "".join(half + middle + half[::-1]), "k": k}
