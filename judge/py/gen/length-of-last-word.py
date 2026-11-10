"""Length of Last Word on 10^4-character strings: many words, or one long word followed by
thousands of trailing spaces."""

SEEDS = 2
N = 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate(rng):
    if rng.random() < 0.5:
        chars = [rng.choice(LETTERS + "  ") for _ in range(N)]
        chars[rng.randrange(N)] = rng.choice(LETTERS)
        return {"s": "".join(chars)}
    word = "".join(rng.choice(LETTERS) for _ in range(rng.randint(1000, 4000)))
    pad = N - len(word) - rng.randint(0, 100)
    return {"s": " " * (N - len(word) - pad) + word + " " * pad}
