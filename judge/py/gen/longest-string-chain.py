"""Longest String Chain with 1000 words: a planted chain of length 16 plus many words that
share its letters, or random words of every length."""

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    words = set()
    if rng.random() < 0.5:
        for _ in range(rng.randint(3, 8)):
            word = ""
            for _ in range(16):
                i = rng.randint(0, len(word))
                word = word[:i] + rng.choice("abc") + word[i:]
                words.add(word)
    while len(words) < 1000:
        n = rng.randint(1, 16)
        words.add("".join(rng.choice("abc" if n < 8 else LETTERS) for _ in range(n)))
    words = sorted(words)
    rng.shuffle(words)
    return {"words": words}
