"""Diagonal Traverse II with 10^5 numbers: one row of 5 * 10^4 among 5 * 10^4 single-number
rows, so walking every diagonal of the bounding box visits ~2.5 * 10^9 cells."""

SEEDS = 2
ROWS = 5 * 10**4
WIDE = 5 * 10**4


def generate(rng):
    long_row = rng.choice([0, rng.randrange(ROWS)])
    nums = []
    for i in range(ROWS):
        width = WIDE if i == long_row else 1
        nums.append([rng.randint(1, 10**5) for _ in range(width)])
    return {"nums": nums}
