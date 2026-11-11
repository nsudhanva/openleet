"""Find Minimum Time to Reach Last Room II on a ~20 x 750 grid: an open top row over a row of
gates that open earlier the further right they are, so each later gate floods the room below
again and a FIFO queue (SPFA) or full sweeps do ~m^2 rows of relaxations; the exit is at the
room's far left corner, so Dijkstra too settles every room."""

SEEDS = 2
ROWS = 20
COLS = 750
WALL = 10**9


def generate(rng):
    rows = ROWS + rng.randint(0, 4)
    # A gate costs at least as much as walking the top row to it, so entering at gate j takes
    # about gate[j]; a gate one column right opens 3-12 earlier, more than the extra step.
    base = 3 * COLS + rng.randint(0, 1000)
    gate, t = [0] * COLS, base
    for j in range(COLS - 1, -1, -1):
        gate[j] = t
        t += rng.randint(3, 12)
    grid = [[0] * COLS, gate]
    grid += [[rng.randint(0, 9) for _ in range(COLS)] for _ in range(rows - 4)]
    # The last row is reached only through the bottom-left corner of the room.
    grid.append([0] + [WALL] * (COLS - 1))
    grid.append([0] * COLS)
    return {"moveTime": grid}
