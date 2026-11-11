"""Sum of Prefix Scores of Strings at 1000 words of length 300 sharing long prefixes, so counting
the words that start with each prefix of each word is ~3 * 10^8 prefix checks."""

SEEDS = 2
N = 1000
L = 300


def generate(rng):
    stems = ["".join(rng.choice("ab") for _ in range(L)) for _ in range(rng.randint(2, 6))]
    words = []
    for _ in range(N):
        stem = rng.choice(stems)
        cut = rng.randint(L // 2, L)
        words.append(stem[:cut] + "".join(rng.choice("abc") for _ in range(L - cut)))
    return {"words": words}
