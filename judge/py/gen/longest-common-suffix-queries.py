"""Longest Common Suffix Queries with 3,000 container words and 3,000 queries built from shared
suffix families, so comparing each query with every container word costs ~10^8 steps."""

SEEDS = 2
C = 3000
Q = 3000


def generate(rng):
    letters = "abcdefghijklmnopqrstuvwxyz"
    families = ["".join(rng.choice("ab") for _ in range(rng.randint(5, 15))) for _ in range(40)]

    def word():
        suffix = rng.choice(families)
        suffix = suffix[rng.randrange(len(suffix)) :]
        return "".join(rng.choice(letters) for _ in range(rng.randint(0, 10))) + suffix

    return {"wordsContainer": [word() for _ in range(C)], "wordsQuery": [word() for _ in range(Q)]}
