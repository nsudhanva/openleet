"""Make Number of Distinct Characters Equal at 5000 letters per word: one word uses x letters, the
other x - 2 of them, each letter at least twice, so no swap closes the gap of 2 and trying every
index pair is the full 2.5 * 10^7 swaps."""

from string import ascii_lowercase

SEEDS = 2
N = 5000


def generate(rng):
    x = rng.randint(4, 26)
    first = rng.sample(ascii_lowercase, x)
    second = rng.sample(first, x - 2)
    word1 = [*first, *first, *(rng.choice(first) for _ in range(N - 2 * x))]
    word2 = [*second, *second, *(rng.choice(second) for _ in range(N - 2 * (x - 2)))]
    rng.shuffle(word1)
    rng.shuffle(word2)
    if rng.random() < 0.5:
        word1, word2 = word2, word1
    return {"word1": "".join(word1), "word2": "".join(word2)}
