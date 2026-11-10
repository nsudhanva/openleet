"""Surrounded Regions on a 200 x 200 board: a serpentine 'O' corridor touching the border (one
40,000-step DFS chain), all 'O', or random."""

SEEDS = 3
SIZE = 200


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        board = [["X"] * SIZE for _ in range(SIZE)]
        for r in range(0, SIZE, 2):
            for c in range(SIZE):
                board[r][c] = "O"
            if r + 1 < SIZE:
                board[r + 1][SIZE - 1 if (r // 2) % 2 == 0 else 0] = "O"
        # Cut the corridor off the border except at one end so most of it must flip or not.
        if rng.random() < 0.5:
            for r in range(SIZE):
                board[r][0] = board[r][SIZE - 1] = "X"
            for c in range(SIZE):
                board[0][c] = board[SIZE - 1][c] = "X"
    elif shape == 1:
        board = [["O"] * SIZE for _ in range(SIZE)]
    else:
        p = rng.uniform(0.3, 0.6)
        board = [["O" if rng.random() < p else "X" for _ in range(SIZE)] for _ in range(SIZE)]
    return {"board": board}
