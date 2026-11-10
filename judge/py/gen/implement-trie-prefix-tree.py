"""Trie with 3 * 10^4 calls over a tiny alphabet: words sharing long prefixes, a few words of the
maximum 2000 letters, and searches/prefix checks that miss by one letter."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
CALLS = 3 * 10**4


def generate(rng):
    alpha = ascii_lowercase[: rng.choice([2, 26])]
    stems = [random_string(rng, alpha, rng.choice([20, 60])) for _ in range(30)]
    longs = [random_string(rng, alpha, 2000) for _ in range(3)]
    inserted = []
    ops, args = ["Trie"], [[]]
    for c in range(CALLS):
        if c % 300 == 0:
            word = rng.choice(longs)[: rng.randint(1900, 2000)]
        else:
            word = rng.choice(stems)[: rng.randint(1, 60)] + random_string(
                rng, alpha, rng.randint(0, 10)
            )
            if not word:
                word = alpha[0]
        r = rng.random()
        if r < 0.4 or not inserted:
            ops.append("insert")
            inserted.append(word)
        elif r < 0.7:
            ops.append("search")
            if rng.random() < 0.5:
                word = rng.choice(inserted)
                if rng.random() < 0.5 and len(word) > 1:
                    word = word[:-1]
        else:
            ops.append("startsWith")
            if rng.random() < 0.5:
                base = rng.choice(inserted)
                word = base[: rng.randint(1, len(base))]
        args.append([word])
    return {"ops": ops, "args": args}
