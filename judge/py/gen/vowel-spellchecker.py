"""Vowel Spellchecker at 5000 words and 5000 queries over a tiny consonant set, so exact,
case-insensitive and vowel-error matches all collide and first-occurrence order matters."""

SEEDS = 2
N = 5000
VOWELS = "aeiou"


def word(rng):
    out = []
    for _ in range(rng.randint(1, 7)):
        c = rng.choice(VOWELS) if rng.random() < 0.5 else rng.choice("ktn")
        out.append(c.upper() if rng.random() < 0.3 else c)
    return "".join(out)


def generate(rng):
    wordlist = [word(rng) for _ in range(N)]
    queries = []
    for _ in range(N):
        r = rng.random()
        if r < 0.3:
            q = rng.choice(wordlist)
        elif r < 0.6:
            q = "".join(c.swapcase() if rng.random() < 0.5 else c for c in rng.choice(wordlist))
        elif r < 0.9:
            q = "".join(
                rng.choice(VOWELS) if c.lower() in VOWELS else c for c in rng.choice(wordlist)
            )
        else:
            q = word(rng)
        queries.append(q)
    return {"wordlist": wordlist, "queries": queries}
