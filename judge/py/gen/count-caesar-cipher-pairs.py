"""Count Caesar Cipher Pairs with 10^4 words of length 10 (n * m at the maximum 10^5), each a
random shift of one of 400 or 1000 base words (so most words are distinct), so comparing every
pair, even of distinct words only, costs over 3 * 10^7 checks of up to 10 letters."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 10**4
M = 10


def generate(rng):
    bases = [random_string(rng, ascii_lowercase, M) for _ in range(rng.choice((400, 1000)))]
    words = []
    for _ in range(N):
        shift = rng.randrange(26)
        words.append("".join(chr((ord(c) - 97 + shift) % 26 + 97) for c in rng.choice(bases)))
    return {"words": words}
