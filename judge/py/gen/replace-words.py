"""Replace Words with 1000 roots over a two-letter alphabet (long shared prefixes) and a
sentence of 1000 words of length ~990 (about 10^6 characters), so naive prefix scans are slow."""

from _shapes import random_string

SEEDS = 2


def generate(rng):
    alphabet = "ab" if rng.random() < 0.5 else "abc"
    roots = set()
    while len(roots) < 1000:
        roots.add(random_string(rng, alphabet, rng.randint(40, 100)))
    dictionary = sorted(roots)
    rng.shuffle(dictionary)
    words = []
    for _ in range(1000):
        length = rng.randint(900, 990)
        if rng.random() < 0.6:
            root = rng.choice(dictionary)
            tail = random_string(rng, alphabet, max(0, length - len(root)))
            words.append((root + tail)[:length] if len(root) <= length else root)
        else:
            words.append(random_string(rng, alphabet, length))
    return {"dictionary": dictionary, "sentence": " ".join(words)}
