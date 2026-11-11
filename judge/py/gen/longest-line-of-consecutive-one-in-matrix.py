"""Longest Line of Consecutive One in Matrix at m * n = 10^4 as a single row or column of ones with
one zero, so walking each direction from every cell costs ~5 * 10^7 steps."""

SEEDS = 2
SIZE = 10**4


def generate(rng):
    line = [1] * SIZE
    line[rng.randrange(SIZE // 2, SIZE)] = 0
    if rng.random() < 0.5:
        return {"mat": [line]}
    return {"mat": [[x] for x in line]}
