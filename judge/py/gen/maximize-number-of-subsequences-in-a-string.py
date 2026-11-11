"""Maximize Number of Subsequences in a String at |text| = 10^4 over a few letters including both
pattern letters (one seed with a doubled pattern), so trying every insertion point and recounting
is 2 * 10^8 steps."""

from string import ascii_lowercase

from _shapes import pick_shape

SEEDS = 2
N = 10**4


def generate(rng):
    doubled = pick_shape(rng) == 0
    letters = rng.sample(ascii_lowercase, 4)
    pattern = letters[0] * 2 if doubled else letters[0] + letters[1]
    text = "".join(rng.choice(letters) for _ in range(N))
    return {"text": text, "pattern": pattern}
