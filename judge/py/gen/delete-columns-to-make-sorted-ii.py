"""Delete Columns to Make Sorted II with 100 strings of length 100 sharing long common
prefixes, so ties persist across many kept columns."""

SEEDS = 2
N, L = 100, 100
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    alphabet = LETTERS if rng.random() < 0.5 else "ab"
    strs = ["".join(rng.choice(alphabet) for _ in range(L)) for _ in range(N)]
    return {"strs": strs}
