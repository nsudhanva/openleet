"""Count Substrings That Can Be Rearranged to Contain a String I at word1 of length 2 * 10^4
whose only copy of a letter of word2 sits near the end, so growing every start until it
covers word2 costs ~2 * 10^8 steps."""

from _shapes import random_string

SEEDS = 2
N = 2 * 10**4
ALPHABET = "abcdefghijklmnopqrstuvwxy"


def generate(rng):
    word1 = random_string(rng, ALPHABET, N - 1)
    at = N - 1 - rng.randint(0, N // 100)
    word1 = word1[:at] + "z" + word1[at:]
    word2 = "z" + random_string(rng, ALPHABET, rng.randint(1, 9))
    return {"word1": word1, "word2": word2}
