"""To Lower Case at the maximum 100 printable ASCII characters, mixing letters with the
symbols just outside 'A'..'Z' ('@', '[')."""

SEEDS = 2


def generate(rng):
    chars = [chr(c) for c in range(32, 127)] + list("@[AZaz") * 5
    return {"s": "".join(rng.choice(chars) for _ in range(100))}
