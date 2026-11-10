"""Count Unique Characters of All Substrings at length 10^5: all 26 letters at random, or only
a few letters so occurrences are dense."""

SEEDS = 2
N = 10**5


def generate(rng):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if rng.random() < 0.5:
        alphabet = "".join(rng.sample(alphabet, 3))
    return {"s": "".join(rng.choice(alphabet) for _ in range(N))}
