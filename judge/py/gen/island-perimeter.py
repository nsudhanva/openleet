"""Island Perimeter on a 100 x 100 grid holding one large, ragged, lake-free island (grown at
random, then any enclosed water filled in)."""

SEEDS = 3
N = 100


def generate(rng):
    rows, cols = rng.choice([(100, 100), (100, 37), (1, 100)])
    grid = [[0] * cols for _ in range(rows)]
    target = rows * cols * rng.choice([0.3, 0.6])
    r, c = rows // 2, cols // 2
    grid[r][c] = 1
    cells, count = [(r, c)], 1
    while count < target:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            grid[nr][nc] = 1
            cells.append((nr, nc))
            count += 1
    # Water not 4-connected to the outside would be a lake: fill it.
    outside = [[False] * cols for _ in range(rows)]
    stack = [
        (i, j)
        for i in range(rows)
        for j in range(cols)
        if (i in (0, rows - 1) or j in (0, cols - 1)) and grid[i][j] == 0
    ]
    for i, j in stack:
        outside[i][j] = True
    while stack:
        i, j = stack.pop()
        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and not outside[ni][nj] and grid[ni][nj] == 0:
                outside[ni][nj] = True
                stack.append((ni, nj))
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0 and not outside[i][j]:
                grid[i][j] = 1
    return {"grid": grid}
