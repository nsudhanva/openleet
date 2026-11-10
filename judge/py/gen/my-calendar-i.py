"""My Calendar I with the maximum 1000 bookings: many short non-overlapping slots mixed with
conflicting ones over [0, 10^9]."""

SEEDS = 3
CALLS = 1000
TOP = 10**9


def generate(rng):
    ops, args = ["MyCalendar"], [[]]
    span = rng.choice((10**6, 10**3, 10**8))
    for _ in range(CALLS):
        start = rng.randint(0, TOP - 1)
        ops.append("book")
        args.append([start, rng.randint(start + 1, min(TOP, start + span))])
    return {"ops": ops, "args": args}
