"""Maximum Number of Non-Overlapping Substrings at length 10^5: random letters (the span of
each letter covers most of the string), or many short self-contained blocks."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        s = random_string(rng, ascii_lowercase, N)
    else:
        parts, total = [], 0
        while total < N:
            letters = rng.sample(ascii_lowercase, rng.randint(1, 4))
            block = random_string(rng, letters, rng.randint(1, 30))
            block = block[: N - total]
            parts.append(block)
            total += len(block)
        s = "".join(parts)
    return {"s": s}
