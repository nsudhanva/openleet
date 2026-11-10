"""Sort Characters By Frequency on 5 * 10^5 letters and digits with skewed frequencies."""

SEEDS = 2
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate(rng):
    weights = [rng.random() ** 3 for _ in CHARS]
    return {"s": "".join(rng.choices(CHARS, weights=weights, k=5 * 10**5))}
