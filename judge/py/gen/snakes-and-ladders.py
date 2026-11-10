"""Snakes and Ladders on a 20 x 20 board: dense random snakes and ladders, or a board full of
snakes that forces a long (or impossible) walk."""

SEEDS = 3


def generate(rng):
    n = 20
    total = n * n
    rate = rng.choice([0.1, 0.3, 0.6])
    snake_bias = rng.choice([0.5, 0.9])
    board = [[-1] * n for _ in range(n)]
    for label in range(2, total):
        if rng.random() >= rate:
            continue
        if rng.random() < snake_bias:
            dest = rng.randint(1, label - 1)
        else:
            dest = rng.randint(label + 1, total)
        idx = label - 1
        row = n - 1 - idx // n
        col = idx % n if (idx // n) % 2 == 0 else n - 1 - idx % n
        board[row][col] = dest
    return {"board": board}
