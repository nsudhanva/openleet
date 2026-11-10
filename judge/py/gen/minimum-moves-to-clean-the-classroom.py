"""Minimum Moves to Clean the Classroom on a 20 x 20 grid with 10 litter cells, a few reset
cells and obstacles, energy up to 50: the state space is cells x litter masks x energy."""

SEEDS = 3
SIZE = 20


def generate(rng):
    cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    rng.shuffle(cells)
    grid = [["."] * SIZE for _ in range(SIZE)]
    sr, sc = cells[0]
    grid[sr][sc] = "S"
    for r, c in cells[1:11]:
        grid[r][c] = "L"
    resets = rng.randint(0, 8)
    for r, c in cells[11 : 11 + resets]:
        grid[r][c] = "R"
    walls = rng.choice((0, 40, 80))
    for r, c in cells[11 + resets : 11 + resets + walls]:
        grid[r][c] = "X"
    energy = rng.choice((50, rng.randint(10, 50)))
    return {"classroom": ["".join(row) for row in grid], "energy": energy}
