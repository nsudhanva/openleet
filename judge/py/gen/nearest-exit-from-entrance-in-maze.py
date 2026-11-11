"""Nearest Exit from Entrance in Maze at 100 x 100, twelve seeds: mostly 0-3% walls with the
entrance walled into a ring near the centre (usually one gap), so a search from each of the ~350
open border cells crosses most of the maze before it reaches the entrance and a DFS that revisits
cells on shorter paths keeps relaxing; and a corridor of ~6000 cells winding back and forth in
anti-diagonal staircases (steps alternate down and left, then up and right) to the only exit,
which costs a repeated relaxation sweep for every two steps."""

from _shapes import pick_shape

SEEDS = 12
M = 100


def ring_maze(rng, closed):
    walls = rng.choice((0.0, 0.0, 0.03))
    maze = [["+" if rng.random() < walls else "." for _ in range(M)] for _ in range(M)]
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
    return maze, [r, c]


def staircase_maze():
    top = M - 2

    def band(s):
        # cells with i + j in {s, s + 1}, rows ascending
        cells = []
        for i in range(1, top + 1):
            for j in (s - i + 1, s - i):
                if 1 <= j <= top:
                    cells.append((i, j))
        return cells

    maze = [["+"] * M for _ in range(M)]
    bands = []
    s = 2
    while s <= 2 * top - 2:
        bands.append(band(s))
        s += 3
    for cells in bands:
        for i, j in cells:
            maze[i][j] = "."
    # Join band t to band t + 1 through a wall cell at the bottom (even t) or top (odd t) end.
    steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for t in range(len(bands) - 1):
        nxt = set(bands[t + 1])
        joined = False
        for i, j in sorted(bands[t], reverse=(t % 2 == 0)):
            for a, b in ((i + x, j + y) for x, y in steps):
                touches = any((a + x, b + y) in nxt for x, y in steps)
                if maze[a][b] == "+" and 1 <= a <= top and 1 <= b <= top and touches:
                    maze[a][b] = "."
                    joined = True
                    break
            if joined:
                break
    last = max(bands[-1], key=lambda cell: (cell[0] + cell[1], cell[0]))
    maze[last[0] + 1 if last[0] == top else last[0]][last[1] + (last[0] != top)] = "."
    return maze, [1, 1]


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2 and rng.getrandbits(2) < 2:
        maze, entrance = staircase_maze()
    else:
        maze, entrance = ring_maze(rng, shape == 1 and rng.getrandbits(1) == 0)
    return {"maze": maze, "entrance": entrance}
