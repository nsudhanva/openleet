"""Transform to Chessboard at n = 29 or 30: a chessboard with rows and columns shuffled
(solvable), or the same with one cell flipped (impossible)."""

SEEDS = 3


def generate(rng):
    flip = rng.random() < 0.5
    n = rng.choice([29, 30])
    rows = list(range(n))
    cols = list(range(n))
    rng.shuffle(rows)
    rng.shuffle(cols)
    board = [[(rows[r] + cols[c]) % 2 for c in range(n)] for r in range(n)]
    if flip:
        r, c = rng.randrange(n), rng.randrange(n)
        board[r][c] ^= 1
    return {"board": board}
