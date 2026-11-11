"""Shortest Word Distance over 2 * 10^4 words: word1 fills most of the first half and word2 most of
the second, so comparing every pair of their positions is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def word(rng):
    return "".join(rng.choice(LETTERS) for _ in range(rng.randint(1, 10)))


def generate(rng):
    word1 = word(rng)
    word2 = word(rng)
    while word2 == word1:
        word2 = word(rng)
    fillers = [w for w in (word(rng) for _ in range(50)) if w not in (word1, word2)]
    half = N // 2
    words = []
    for i in range(N):
        if rng.random() < 0.05:
            words.append(rng.choice(fillers))
        else:
            words.append(word1 if i < half else word2)
    words[0], words[-1] = word1, word2
    return {"wordsDict": words, "word1": word1, "word2": word2}
