"""Shortest Bridge on a 100 x 100 grid with exactly two islands on opposite sides of an empty
diagonal band: two huge triangles, two random blobs, or two single cells in far corners."""

SEEDS = 3
N = 100


def blob(rng, start, allowed, size):
    cells = {start}
    frontier = [start]
    while frontier and len(cells) < size:
        i = rng.randrange(len(frontier))
        r, c = frontier[i]
        dr, dc = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nr, nc = r + dr, c + dc
        if 0 <= nr < N and 0 <= nc < N and allowed(nr, nc) and (nr, nc) not in cells:
            cells.add((nr, nc))
            frontier.append((nr, nc))
        elif rng.random() < 0.05:
            frontier[i] = frontier[-1]
            frontier.pop()
    return cells


def generate(rng):
    shape = rng.getrandbits(6) % 3
    grid = [[0] * N for _ in range(N)]
    if shape == 0:
        for r in range(N):
            for c in range(N):
                if r + c <= N - 3 or r + c >= N + 1:
                    grid[r][c] = 1
    elif shape == 1:
        a = blob(rng, (0, 0), lambda r, c: r + c <= N - 3, 3000)
        b = blob(rng, (N - 1, N - 1), lambda r, c: r + c >= N + 1, 3000)
        for r, c in a | b:
            grid[r][c] = 1
    else:
        grid[0][0] = 1
        grid[N - 1][N - 1] = 1
    return {"grid": grid}
