"""Sort Vowels in a String at 10^5 letters, nine in ten of them vowels of either case, so
picking the smallest remaining vowel for each vowel slot is ~4 * 10^9 steps."""

from string import ascii_letters

SEEDS = 2
N = 10**5
VOWELS = "aeiouAEIOU"


def generate(rng):
    s = [rng.choice(VOWELS) if rng.random() < 0.9 else rng.choice(ascii_letters) for _ in range(N)]
    return {"s": "".join(s)}
