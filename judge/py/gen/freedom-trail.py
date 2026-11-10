"""Freedom Trail at the maximum lengths (ring and key of 100) over a tiny alphabet, so every key
letter has many ring positions to choose from."""

SEEDS = 3


def generate(rng):
    alpha = "abcdefghijklmnopqrstuvwxyz"[: rng.choice([2, 3, 26])]
    ring = [rng.choice(alpha) for _ in range(100)]
    ring[: len(alpha)] = alpha
    rng.shuffle(ring)
    key = "".join(rng.choice(alpha) for _ in range(100))
    return {"ring": "".join(ring), "key": key}
