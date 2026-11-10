"""Add and Search Words with 10^4 calls: thousands of long words over a tiny alphabet, then
searches with two wildcards that force wide trie branching."""

from _shapes import random_string

SEEDS = 2
CALLS = 10**4


def word(rng, alphabet):
    return random_string(rng, alphabet, rng.randint(15, 25))


def with_dots(rng, w):
    chars = list(w)
    for i in rng.sample(range(len(chars)), min(2, len(chars))):
        chars[i] = "."
    return "".join(chars)


def generate(rng):
    alphabet = "ab" if rng.random() < 0.5 else "abcdefghijklmnopqrstuvwxyz"
    ops, args = ["WordDictionary"], [[]]
    added = []
    for _ in range(CALLS):
        if rng.random() < 0.5 or not added:
            w = word(rng, alphabet)
            added.append(w)
            ops.append("addWord")
            args.append([w])
        else:
            w = rng.choice(added) if rng.random() < 0.5 else word(rng, alphabet)
            if rng.random() < 0.8:
                w = with_dots(rng, w)
            ops.append("search")
            args.append([w])
    return {"ops": ops, "args": args}
