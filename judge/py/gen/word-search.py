"""Word Search on a full 6 x 6 board of one letter with a 15-letter word that fails only on
its last letter: the backtracking worst case; or a random board with a planted path."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        board = [["A"] * 6 for _ in range(6)]
        return {"board": board, "word": "A" * 14 + "B"}
    if shape == 1:
        board = [[rng.choice("aA") for _ in range(6)] for _ in range(6)]
        word = "".join(rng.choice("aA") for _ in range(15))
        return {"board": board, "word": word}
    board = [[rng.choice("abAB") for _ in range(6)] for _ in range(6)]
    # Plant a self-avoiding walk so the word exists.
    while True:
        r, c = rng.randrange(6), rng.randrange(6)
        path = [(r, c)]
        while len(path) < 15:
            steps = [
                (r + dr, c + dc)
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= r + dr < 6 and 0 <= c + dc < 6 and (r + dr, c + dc) not in path
            ]
            if not steps:
                break
            r, c = rng.choice(steps)
            path.append((r, c))
        if len(path) == 15:
            break
    return {"board": board, "word": "".join(board[r][c] for r, c in path)}
