"""Lonely Pixel I on a 400 by 400 picture that is two thirds black with a few lonely pixels, so
counting each black pixel's row and column afresh costs ~10^8 steps."""

SEEDS = 2
M = 400
DENSITY = 0.67


def generate(rng):
    pic = [["B" if rng.random() < DENSITY else "W" for _ in range(M)] for _ in range(M)]
    # Clear a few rows and columns, then put one pixel where each pair crosses.
    lonely = rng.randint(1, max(1, M // 30))
    rows = rng.sample(range(M), lonely)
    cols = rng.sample(range(M), lonely)
    for r in rows:
        pic[r] = ["W"] * M
    for c in cols:
        for row in pic:
            row[c] = "W"
    for r, c in zip(rows, cols, strict=True):
        pic[r][c] = "B"
    return {"picture": pic}
