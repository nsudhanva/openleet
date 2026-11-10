"""Uncommon Words at the 200-char limit with a small vocabulary, so words repeat within and
across the sentences."""

SEEDS = 2
LETTERS = "abcde"


def sentence(rng, vocab):
    words = []
    while True:
        w = rng.choice(vocab)
        if len(" ".join([*words, w])) > 200:
            break
        words.append(w)
    return " ".join(words)


def generate(rng):
    vocab = sorted(
        {"".join(rng.choice(LETTERS) for _ in range(rng.randint(1, 3))) for _ in range(60)}
    )
    return {"s1": sentence(rng, vocab), "s2": sentence(rng, vocab)}
