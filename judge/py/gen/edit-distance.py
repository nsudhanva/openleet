"""Edit Distance at 500 x 500: random words, or one a light mutation of the other."""

from string import ascii_lowercase

SEEDS = 2
L = 500


def generate(rng):
    word1 = [rng.choice(ascii_lowercase) for _ in range(L)]
    if rng.random() < 0.5:
        word2 = [rng.choice(ascii_lowercase) for _ in range(L)]
    else:
        word2 = word1[:]
        for _ in range(50):
            word2[rng.randrange(L)] = rng.choice(ascii_lowercase)
    return {"word1": "".join(word1), "word2": "".join(word2)}
