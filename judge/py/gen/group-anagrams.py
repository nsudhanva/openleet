"""Group Anagrams with 10^4 strings of up to 100 letters: large anagram groups of long strings,
plus empty strings and near-anagrams that differ by one letter."""

from _shapes import random_string

SEEDS = 2
N = 10**4


def generate(rng):
    alpha = "abcdefghijklmnopqrstuvwxyz"[: rng.choice([3, 26])]
    bases = [random_string(rng, alpha, rng.randint(0, 100)) for _ in range(300)]
    strs = []
    for _ in range(N):
        chars = list(rng.choice(bases))
        rng.shuffle(chars)
        if chars and rng.random() < 0.1:
            chars[0] = rng.choice(alpha)
        strs.append("".join(chars))
    return {"strs": strs}
