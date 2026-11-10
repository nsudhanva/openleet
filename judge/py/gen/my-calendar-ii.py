"""My Calendar II with the maximum 1000 bookings over a narrow range so double bookings are
common and triple bookings must be rejected."""

SEEDS = 3
CALLS = 1000


def generate(rng):
    ops, args = ["MyCalendarTwo"], [[]]
    top = rng.choice((10**4, 10**6, 10**9))
    span = max(1, top // rng.choice((50, 500)))
    for _ in range(CALLS):
        start = rng.randint(0, top - 1)
        ops.append("book")
        args.append([start, rng.randint(start + 1, min(top, start + span))])
    return {"ops": ops, "args": args}
