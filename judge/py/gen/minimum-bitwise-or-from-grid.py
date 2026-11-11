"""Minimum Bitwise OR From Grid with 2000 rows of 20 values, one or two of bits 0-15 in every row
but the last, whose values all carry bit 16, so the reachable ORs grow to about 2^16 and an
increasing scan of candidate ORs fails every candidate below 2^16 only at the last row."""

SEEDS = 2
ROWS = 2000
COLS = 20
BITS = 17


def generate(rng):
    grid = []
    for _ in range(ROWS - 1):
        row = []
        for _ in range(COLS):
            x = 1 << rng.randrange(BITS - 1)
            if rng.random() < 0.5:
                x |= 1 << rng.randrange(BITS - 1)
            row.append(x)
        grid.append(row)
    # The low part stays under 2^15 so every value is at most 98303, within 10^5.
    grid.append([(1 << (BITS - 1)) | rng.randrange(1 << (BITS - 2)) for _ in range(COLS)])
    return {"grid": grid}
