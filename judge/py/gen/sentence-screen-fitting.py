"""Sentence Screen Fitting with rows = cols = 2 * 10^4 and 100 words of one to three letters, so
placing words one at a time fills ~10^4 words per row, ~10^8 in all."""

SEEDS = 2
ROWS = COLS = 2 * 10**4
WORDS = 100


def generate(rng):
    top = rng.choice([1, 3])
    sentence = [
        "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(1, top)))
        for _ in range(WORDS)
    ]
    return {"sentence": sentence, "rows": ROWS, "cols": COLS - rng.randrange(10)}
