"""Battleships in a Board at 200 x 200: 10^4 single-cell ships on a lattice, or many random
horizontal and vertical ships kept apart so the board is valid."""

SEEDS = 2
SIZE = 200


def generate(rng):
    m, n = SIZE, SIZE
    board = [["."] * n for _ in range(m)]
    if rng.random() < 0.4:
        for r in range(0, m, 2):
            for c in range(0, n, 2):
                board[r][c] = "X"
        return {"board": board}
    for _ in range(6000):
        length = rng.randint(1, 8)
        horizontal = rng.random() < 0.5
        r = rng.randrange(m - (0 if horizontal else length - 1))
        c = rng.randrange(n - (length - 1 if horizontal else 0))
        cells = [(r, c + i) if horizontal else (r + i, c) for i in range(length)]
        # Reject if any cell or any neighbour (8 directions) is already a ship.
        clear = all(
            board[y][x] == "."
            for cr, cc in cells
            for y in range(max(0, cr - 1), min(m, cr + 2))
            for x in range(max(0, cc - 1), min(n, cc + 2))
        )
        if clear:
            for cr, cc in cells:
                board[cr][cc] = "X"
    return {"board": board}
