"""Count Unguarded Cells at m * n ~ 10^5: one row (or column) holding 5 * 10^4 guards and a
guard-free stretch between two walls, so guards that look past other guards walk ~10^9 cells, or
a 316 x 316 grid with two guards and walls, so scanning outward from every cell costs ~6 * 10^7
steps."""

from _shapes import pick_shape

SEEDS = 3
CELLS = 10**5
GUARDS = 5 * 10**4
SIDE = 316
GAP = 300  # unguarded cells walled off from the guards in the line shapes


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2:
        m = n = SIDE
        cells = rng.sample(range(m * n), 4)
        guards, walls = cells[:2], cells[2:]
    else:
        m, n = 1, CELLS
        left = rng.randrange(CELLS - GAP - 1)
        right = left + rng.randint(GAP // 2, GAP) + 1
        free = [c for c in range(CELLS) if not left <= c <= right]
        cells = rng.sample(free, GUARDS + 1)
        guards, walls = cells[:GUARDS], [left, right, cells[GUARDS]]
        if shape == 1:
            m, n = n, m
    return {
        "m": m,
        "n": n,
        "guards": [[c // n, c % n] for c in guards],
        "walls": [[c // n, c % n] for c in walls],
    }
