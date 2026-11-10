"""Shortest Completing Word with a 7-character plate (repeated letters, mixed case, digits,
spaces) and 1000 words of length <= 15, several of which complete it."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    plate_letters = [rng.choice("abcde") for _ in range(rng.randint(3, 5))]
    plate = [c.upper() if rng.random() < 0.5 else c for c in plate_letters]
    while len(plate) < 7:
        plate.insert(rng.randint(0, len(plate)), rng.choice("0123456789 "))
    words = []
    for _ in range(1000):
        if rng.random() < 0.2:
            w = plate_letters + [
                rng.choice(ascii_lowercase) for _ in range(rng.randint(0, 15 - len(plate_letters)))
            ]
            rng.shuffle(w)
            words.append("".join(w))
        else:
            words.append(random_string(rng, "abcdefgh", rng.randint(1, 15)))
    return {"licensePlate": "".join(plate), "words": words}
