"""Short Encoding with 2000 words of length <= 7 over a tiny alphabet, so many words are
suffixes of others (and some repeat)."""

SEEDS = 2


def generate(rng):
    alphabet = rng.choice(["ab", "abc", "abcdefghijklmnopqrstuvwxyz"])
    words = []
    for _ in range(2000):
        words.append("".join(rng.choice(alphabet) for _ in range(rng.randint(1, 7))))
    return {"words": words}
