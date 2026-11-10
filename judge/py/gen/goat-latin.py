"""Goat Latin at up to 150 characters: many short words (the 'a' suffix grows fastest) mixing
upper- and lowercase vowels and consonants."""

SEEDS = 2
LETTERS = "aeiouAEIOUbcdfgBCDFGxyzXYZ"


def generate(rng):
    words, length = [], 0
    while True:
        w = "".join(rng.choice(LETTERS) for _ in range(rng.randint(1, 3)))
        extra = len(w) + (1 if words else 0)
        if length + extra > 150:
            break
        words.append(w)
        length += extra
    return {"sentence": " ".join(words)}
