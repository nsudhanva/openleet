"""Edit Distance at 500 x 500: random words, or one a light mutation of the other."""

SEEDS = 2
L = 500
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    word1 = [rng.choice(LETTERS) for _ in range(L)]
    if rng.random() < 0.5:
        word2 = [rng.choice(LETTERS) for _ in range(L)]
    else:
        word2 = word1[:]
        for _ in range(50):
            word2[rng.randrange(L)] = rng.choice(LETTERS)
    return {"word1": "".join(word1), "word2": "".join(word2)}
