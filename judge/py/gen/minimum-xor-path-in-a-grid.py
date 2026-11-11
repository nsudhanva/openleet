"""Minimum XOR Path at 16 x 16 (paths of 31 cells, an odd count). One seed has random values below
1024; in the others every value has the same low bit or the top bit set, so no path XORs to 0 and a
search that stops at the first zero still has to look at all of the C(30, 15) ~ 1.6 * 10^8
monotone paths, while tracking the reachable XOR set per cell is ~2.6 * 10^5 steps."""

from _shapes import pick_shape

SEEDS = 3
M = 16


def generate(rng):
    shape = pick_shape(rng)
    grid = [[rng.randrange(1024) for _ in range(M)] for _ in range(M)]
    if shape == 1:
        grid = [[v | 1 for v in row] for row in grid]
    elif shape == 2:
        grid = [[v | 512 for v in row] for row in grid]
    return {"grid": grid}
