"""Jewels and Stones at the maximum 50 characters each, mixing cases."""

from string import ascii_letters

SEEDS = 2


def generate(rng):
    jewels = "".join(rng.sample(ascii_letters, 50))
    stones = "".join(rng.choice(ascii_letters[: rng.choice([4, 52])]) for _ in range(50))
    if rng.random() < 0.5:
        jewels = jewels[: rng.randint(1, 10)]
    return {"jewels": jewels, "stones": stones}
