"""Sort Characters By Frequency on 5 * 10^5 letters and digits with skewed frequencies."""

from string import ascii_letters, digits

SEEDS = 2
CHARS = ascii_letters + digits


def generate(rng):
    weights = [rng.random() ** 3 for _ in CHARS]
    return {"s": "".join(rng.choices(CHARS, weights=weights, k=5 * 10**5))}
