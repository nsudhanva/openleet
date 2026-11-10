"""Replace Words with 1000 roots over a two-letter alphabet (long shared prefixes) and a
sentence of 1000 words of length ~990 (about 10^6 characters), so naive prefix scans are slow."""

SEEDS = 2


def generate(rng):
    alphabet = "ab" if rng.random() < 0.5 else "abc"
    roots = set()
    while len(roots) < 1000:
        roots.add("".join(rng.choice(alphabet) for _ in range(rng.randint(40, 100))))
    dictionary = sorted(roots)
    rng.shuffle(dictionary)
    words = []
    for _ in range(1000):
        length = rng.randint(900, 990)
        if rng.random() < 0.6:
            root = rng.choice(dictionary)
            tail = "".join(rng.choice(alphabet) for _ in range(max(0, length - len(root))))
            words.append((root + tail)[:length] if len(root) <= length else root)
        else:
            words.append("".join(rng.choice(alphabet) for _ in range(length)))
    return {"dictionary": dictionary, "sentence": " ".join(words)}
