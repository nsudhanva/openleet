"""Sort Vowels in a String at 10^5 letters, nine in ten of them vowels of either case, in random
order or with the vowels in descending order (each insertion into a sorted list lands near the
front), so picking the smallest remaining vowel for each vowel slot is ~4 * 10^9 steps and
inserting into a sorted list moves ~3 * 10^9 elements."""

from string import ascii_letters

from _shapes import pick_shape

SEEDS = 2
N = 10**5
VOWELS = "aeiouAEIOU"


def generate(rng):
    shape = pick_shape(rng)
    s = [rng.choice(VOWELS) if rng.random() < 0.9 else rng.choice(ascii_letters) for _ in range(N)]
    if shape != 0:
        slots = [i for i, c in enumerate(s) if c in VOWELS]
        for i, c in zip(slots, sorted((s[i] for i in slots), reverse=True), strict=True):
            s[i] = c
    return {"s": "".join(s)}
