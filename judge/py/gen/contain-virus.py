"""Contain Virus on a 50 x 50 grid seeded with scattered infected blobs, so the simulation
runs many rounds; each grid is simulated here and kept only when no round has a tie."""

SEEDS = 2
M = N = 50
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def no_ties(grid):
    g = [row[:] for row in grid]
    while True:
        seen = [[False] * N for _ in range(M)]
        regions = []
        for r in range(M):
            for c in range(N):
                if g[r][c] == 1 and not seen[r][c]:
                    seen[r][c] = True
                    cells, threat, stack = [], set(), [(r, c)]
                    while stack:
                        x, y = stack.pop()
                        cells.append((x, y))
                        for dx, dy in DIRS:
                            a, b = x + dx, y + dy
                            if 0 <= a < M and 0 <= b < N:
                                if g[a][b] == 0:
                                    threat.add((a, b))
                                elif g[a][b] == 1 and not seen[a][b]:
                                    seen[a][b] = True
                                    stack.append((a, b))
                    regions.append((len(threat), cells, threat))
        if not regions:
            return True
        regions.sort(key=lambda t: -t[0])
        if regions[0][0] == 0:
            return True
        if len(regions) > 1 and regions[1][0] == regions[0][0]:
            return False
        for x, y in regions[0][1]:
            g[x][y] = 2
        for _, _, threat in regions[1:]:
            for a, b in threat:
                g[a][b] = 1


def generate(rng):
    while True:
        grid = [[0] * N for _ in range(M)]
        for _ in range(rng.randint(4, 12)):
            r, c = rng.randrange(M), rng.randrange(N)
            for _ in range(rng.randint(1, 15)):
                grid[r][c] = 1
                dr, dc = rng.choice(DIRS)
                r = min(M - 1, max(0, r + dr))
                c = min(N - 1, max(0, c + dc))
        if no_ties(grid):
            return {"isInfected": grid}
