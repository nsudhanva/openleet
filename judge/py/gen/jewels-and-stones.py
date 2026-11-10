"""Jewels and Stones at the maximum 50 characters each, mixing cases."""

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate(rng):
    jewels = "".join(rng.sample(LETTERS, 50))
    stones = "".join(rng.choice(LETTERS[: rng.choice([4, 52])]) for _ in range(50))
    if rng.random() < 0.5:
        jewels = jewels[: rng.randint(1, 10)]
    return {"jewels": jewels, "stones": stones}
