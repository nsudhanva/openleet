"""Swim in Rising Water on the maximum 50 x 50 grid: values in a random growth order from the
start (every lower set is one connected region), the far corner low and walled in by the two
highest, so the answer is n^2 - 2 and a fresh search for each time t from max(start, corner)
visits ~n^4 / 2 cells."""

SEEDS = 2
N = 50


def generate(rng):
    cells = N * N
    corner, walls = cells - 1, [cells - 2, cells - N - 1]
    rng.shuffle(walls)
    flat = [0] * cells
    flat[walls[0]], flat[walls[1]] = cells - 1, cells - 2
    # A small value for the corner, which the growth order then skips.
    low = flat[corner] = rng.randint(1, min(N, cells - 3))
    seen = {0, corner, *walls}
    frontier, value = [0], 0
    while frontier:
        j = rng.randrange(len(frontier))
        frontier[j], frontier[-1] = frontier[-1], frontier[j]
        cell = frontier.pop()
        value += value == low
        flat[cell] = value
        value += 1
        r, c = divmod(cell, N)
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < N and 0 <= y < N and x * N + y not in seen:
                seen.add(x * N + y)
                frontier.append(x * N + y)
    return {"grid": [flat[r * N : (r + 1) * N] for r in range(N)]}
