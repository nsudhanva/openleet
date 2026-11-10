"""Number of Segments at the maximum length 300, with runs of spaces and every allowed symbol."""

SEEDS = 2
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=',.:"


def generate(rng):
    space = rng.choice([0.2, 0.5])
    s = "".join(" " if rng.random() < space else rng.choice(ALPHABET) for _ in range(300))
    return {"s": s}
