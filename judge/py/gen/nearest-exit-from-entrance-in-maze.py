"""Nearest Exit from Entrance in Maze at 100 x 100 with ~10% walls and the entrance walled into
a ring near the centre (with one gap on one seed, none on the other), so a search from each of
the ~350 open border cells crosses most of the maze before it reaches the entrance."""

SEEDS = 2
M = 100


def generate(rng):
    closed = rng.randrange(2)  # seed 0 has no way out, seed 1 one gap in the ring
    maze = [["+" if rng.random() < 0.1 else "." for _ in range(M)] for _ in range(M)]
    r, c = rng.randrange(M // 3, 2 * M // 3), rng.randrange(M // 3, 2 * M // 3)
    ring = [
        (i, j)
        for i in range(M)
        for j in range(M)
        if max(abs(i - r), abs(j - c)) == M // 6 and 0 < i < M - 1 and 0 < j < M - 1
    ]
    for i, j in ring:
        maze[i][j] = "+"
    if not closed:
        i, j = rng.choice([(i, j) for i, j in ring if abs(i - r) != abs(j - c)])
        maze[i][j] = "."
    maze[r][c] = "."
    return {"maze": maze, "entrance": [r, c]}
