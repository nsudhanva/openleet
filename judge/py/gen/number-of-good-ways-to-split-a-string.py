"""Number of Good Ways to Split a String at 5 * 10^4 letters over a random-sized alphabet, so
counting the distinct letters of both halves afresh at every split costs ~2.5 * 10^9 steps."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    alphabet = rng.sample(ascii_lowercase, rng.randint(8, 26))
    return {"s": random_string(rng, alphabet, N)}
