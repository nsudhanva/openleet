"""Stickers to Spell Word with 50 stickers and a 15-letter target: many letters, each sticker
covering only a few, so the 2^15 state search is fully explored (sometimes impossible)."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 3


def generate(rng):
    pool = rng.sample(ascii_lowercase, rng.choice([8, 12, 15]))
    target = random_string(rng, pool, 15)
    stickers = []
    for _ in range(50):
        length = rng.randint(1, 10)
        stickers.append(
            "".join(
                rng.choice(pool) if rng.random() < 0.3 else rng.choice(ascii_lowercase)
                for _ in range(length)
            )
        )
    if rng.random() < 0.3:
        # Remove one target letter from every sticker: answer -1.
        gone = target[0]
        stickers = [s.replace(gone, "z" if gone != "z" else "y") for s in stickers]
    return {"stickers": stickers, "target": target}
