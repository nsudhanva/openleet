"""Smallest Palindromic Rearrangement II at length 10^4 with k near 10^6 and at least k
arrangements (many letters, or a few rare letters among 'a's), so stepping through the
permutations one at a time takes ~10^6 steps."""

from string import ascii_lowercase

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    n = rng.choice([10**4, 10**4 - 1])
    m = n // 2
    if shape == 0:
        half = [rng.choice(ascii_lowercase) for _ in range(m)]
    elif shape == 1:
        # Two letters, three of them rare: C(5000, 3) arrangements.
        half = ["a"] * m
        for i in rng.sample(range(m), 3):
            half[i] = "b"
    else:
        # One 'b' and one 'c' among 'a's: m * (m - 1) arrangements.
        half = ["a"] * (m - 2) + ["b", "c"]
    rng.shuffle(half)
    middle = [rng.choice("abc")] if n % 2 else []
    k = rng.randint(9 * 10**5, 10**6)
    return {"s": "".join(half + middle + half[::-1]), "k": k}
