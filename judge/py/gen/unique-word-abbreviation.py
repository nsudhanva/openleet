"""Unique Word Abbreviation at 3 * 10^4 dictionary words and 5000 isUnique calls, nearly all
true (dictionary words alone in their abbreviation, or words of lengths the dictionary lacks),
so scanning the dictionary per call is ~1.5 * 10^8 steps."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
WORDS = 3 * 10**4
CALLS = 5000


def generate(rng):
    dictionary = [random_string(rng, ascii_lowercase, rng.randint(1, 14)) for _ in range(WORDS)]
    abbr = {}
    for w in dictionary:
        abbr.setdefault((w[0], w[-1], len(w)) if len(w) > 2 else w, set()).add(w)
    alone = sorted(w for group in abbr.values() if len(group) == 1 for w in group)
    ops: list = ["ValidWordAbbr"]
    args: list = [[dictionary]]
    for _ in range(CALLS):
        r = rng.random()
        if r < 0.05:
            # A new word sharing a dictionary word's abbreviation: false unless it is that word.
            w = rng.choice(dictionary)
            word = (
                w[0] + random_string(rng, ascii_lowercase, len(w) - 2) + w[-1] if len(w) > 2 else w
            )
        elif r < 0.5:
            word = rng.choice(alone)
        else:
            word = random_string(rng, ascii_lowercase, rng.randint(15, 20))
        ops.append("isUnique")
        args.append([word])
    return {"ops": ops, "args": args}
