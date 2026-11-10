"""Minesweeper on a 50 x 50 unrevealed board with sparse mines, clicked on an empty cell so
the reveal floods most of the board."""

SEEDS = 3
SIZE = 50


def generate(rng):
    density = rng.choice((0.0, 0.02, 0.08))
    board = [["M" if rng.random() < density else "E" for _ in range(SIZE)] for _ in range(SIZE)]
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == "E"]
    r, c = rng.choice(empty)
    return {"board": board, "click": [r, c]}
