"""My Calendar III with the maximum 400 bookings, heavily overlapping over [0, 10^9]."""

SEEDS = 3
CALLS = 400
TOP = 10**9


def generate(rng):
    ops, args = ["MyCalendarThree"], [[]]
    span = rng.choice((10**9, 10**7))
    for _ in range(CALLS):
        start = rng.randint(0, TOP - 1)
        ops.append("book")
        args.append([start, rng.randint(start + 1, min(TOP, start + span))])
    return {"ops": ops, "args": args}
