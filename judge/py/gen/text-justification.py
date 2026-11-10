"""Text Justification at the maximum 300 words with widths that force uneven space splits,
single-word lines, and a width equal to the longest word."""

SEEDS = 3
N = 300
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,;:!?'-()"


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        width = rng.randint(20, 100)
        top = 20
    elif shape == 1:
        width = rng.randint(1, 6)
        top = width
    else:
        width = 20
        top = 20
    words = ["".join(rng.choice(CHARS) for _ in range(rng.randint(1, top))) for _ in range(N)]
    return {"words": words, "maxWidth": width}
