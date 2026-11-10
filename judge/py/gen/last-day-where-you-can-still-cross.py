"""Last Day to Cross with row * col = 2 * 10^4 cells flooded in random order, on a square,
very wide, or very tall grid; rerunning a BFS every day is quadratic."""

SEEDS = 3


def generate(rng):
    row, col = rng.choice([(100, 200), (2, 10**4), (10**4, 2), (200, 100)])
    cells = [[r, c] for r in range(1, row + 1) for c in range(1, col + 1)]
    rng.shuffle(cells)
    return {"row": row, "col": col, "cells": cells}
