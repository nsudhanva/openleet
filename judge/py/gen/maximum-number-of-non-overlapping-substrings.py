"""Maximum Number of Non-Overlapping Substrings at length 10^5: random letters (the span of
each letter covers most of the string), or many short self-contained blocks."""

SEEDS = 2
N = 10**5
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    if rng.random() < 0.5:
        s = "".join(rng.choice(LETTERS) for _ in range(N))
    else:
        parts, total = [], 0
        while total < N:
            letters = rng.sample(LETTERS, rng.randint(1, 4))
            block = "".join(rng.choice(letters) for _ in range(rng.randint(1, 30)))
            block = block[: N - total]
            parts.append(block)
            total += len(block)
        s = "".join(parts)
    return {"s": s}
