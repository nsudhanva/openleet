"""Prefix and Suffix Search with 10^4 words and 10^4 queries over a two-letter alphabet, so
every prefix and suffix matches thousands of words and scanning the list per query is slow."""

from _shapes import random_string

SEEDS = 2
WORDS = 10**4
CALLS = 10**4


def generate(rng):
    alpha = rng.choice(["ab", "abc"])
    words = [random_string(rng, alpha, rng.randint(1, 7)) for _ in range(WORDS)]
    ops: list[str] = ["WordFilter"]
    args: list[list] = [[words]]
    for _ in range(CALLS):
        if rng.random() < 0.7:
            w = rng.choice(words)
            pref = w[: rng.randint(1, len(w))]
            w2 = rng.choice(words) if rng.random() < 0.3 else w
            suff = w2[-rng.randint(1, len(w2)) :]
        else:
            pref = random_string(rng, "abcz", rng.randint(1, 7))
            suff = random_string(rng, "abcz", rng.randint(1, 7))
        ops.append("f")
        args.append([pref, suff])
    return {"ops": ops, "args": args}
