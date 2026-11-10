"""Determine if Two Strings Are Close at length 10^5: word2 built by permuting word1 and
swapping letter roles (answer true), or the same with one letter changed."""

from string import ascii_lowercase

SEEDS = 2
N = 10**5


def generate(rng):
    alphabet = rng.sample(ascii_lowercase, rng.randint(2, 26))
    word1 = [rng.choice(alphabet) for _ in range(N)]
    shuffled = alphabet[:]
    rng.shuffle(shuffled)
    mapping = dict(zip(alphabet, shuffled, strict=True))
    word2 = [mapping[c] for c in word1]
    rng.shuffle(word2)
    if rng.random() < 0.5:
        word2[rng.randrange(N)] = rng.choice(ascii_lowercase)
    return {"word1": "".join(word1), "word2": "".join(word2)}
