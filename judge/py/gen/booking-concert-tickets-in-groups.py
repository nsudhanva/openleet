"""Booking Concert Tickets at 5 * 10^4 rows and 4 * 10^4 calls: 1.2 * 10^4 gathers that each fill
the next row but a few seats; 2 * 10^4 scatters asking one seat more than rows 0..maxRow hold
(maxRow anywhere past the filled rows) and gathers that fit nowhere, both changing nothing; then
small scatters mixed with gathers that fit only past the filled rows: scanning rows is ~10^9."""

SEEDS = 2
ROWS = 5 * 10**4
CALLS = 4 * 10**4


def generate(rng):
    m = rng.choice([2 * 10**4, 1000])
    fill = CALLS * 3 // 10
    ops, args = ["BookMyShow"], [[ROWS, m]]
    left = 0  # seats still free in rows 0..fill-1; later rows stay empty until the last phase
    for _ in range(fill):
        free = rng.randint(1, 10)
        left += free
        ops.append("gather")
        args.append([m - free, ROWS - 1])
    top = min(ROWS - 1, fill - 1 + (10**9 - 1 - left) // m)
    while len(ops) - 1 < CALLS * 8 // 10:
        if rng.random() < 0.8:
            row = rng.randint(fill, top)
            ops.append("scatter")
            args.append([left + (row - fill + 1) * m + 1, row])
        else:
            ops.append("gather")
            args.append([rng.randint(11, m), rng.randrange(fill)])
    while len(ops) - 1 < CALLS:
        r = rng.random()
        if r < 0.6:
            ops.append("scatter")
            args.append([rng.randint(1, 20), ROWS - 1])
        elif r < 0.85:
            ops.append("gather")
            args.append([rng.randint(11, m), rng.randint(fill, ROWS - 1)])
        else:
            ops.append("gather")
            args.append([rng.randint(11, m), rng.randrange(fill)])
    return {"ops": ops, "args": args}
