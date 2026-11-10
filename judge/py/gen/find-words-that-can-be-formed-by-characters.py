"""Find Words That Can Be Formed by Characters with 1000 words of up to 100 letters drawn from
the same pool as chars, so many words fit or just miss."""

SEEDS = 2


def generate(rng):
    alpha = "abcdefghijklmnopqrstuvwxyz"[: rng.choice([4, 26])]
    chars = "".join(rng.choice(alpha) for _ in range(100))
    words = []
    for _ in range(1000):
        if rng.random() < 0.5:
            pool = list(chars)
            rng.shuffle(pool)
            words.append("".join(pool[: rng.randint(1, 100)]))
        else:
            words.append("".join(rng.choice(alpha) for _ in range(rng.randint(1, 100))))
    return {"words": words, "chars": chars}
