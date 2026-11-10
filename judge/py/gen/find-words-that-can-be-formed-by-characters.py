"""Find Words That Can Be Formed by Characters with 1000 words of up to 100 letters drawn from
the same pool as chars, so many words fit or just miss."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    alpha = ascii_lowercase[: rng.choice([4, 26])]
    chars = random_string(rng, alpha, 100)
    words = []
    for _ in range(1000):
        if rng.random() < 0.5:
            pool = list(chars)
            rng.shuffle(pool)
            words.append("".join(pool[: rng.randint(1, 100)]))
        else:
            words.append(random_string(rng, alpha, rng.randint(1, 100)))
    return {"words": words, "chars": chars}
