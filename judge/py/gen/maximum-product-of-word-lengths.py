"""Maximum Product of Word Lengths with 1000 words of up to 1000 letters each, drawn from
small random alphabets so only some pairs share no letter; pairwise set comparison is slow."""

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    words = []
    for _ in range(1000):
        alphabet = rng.sample(LETTERS, rng.randint(1, 13))
        length = rng.randint(1, 1000)
        words.append("".join(rng.choice(alphabet) for _ in range(length)))
    return {"words": words}
