"""My Calendar II with the maximum 1000 bookings over [0, 10^9]: 500 back-to-back bookings tiling
the range, a copy of the last one, then 499 that reach into it and would triple there, so checking
pairs of accepted bookings, even only those that meet the new one, is ~5 * 10^7 steps."""

from itertools import pairwise

SEEDS = 2
TILES = 500
TOP = 10**9


def generate(rng):
    cuts = [0, *sorted(rng.sample(range(1, TOP), TILES - 1)), TOP]
    args = [[], *([a, b] for a, b in pairwise(cuts))]
    last = cuts[-2]
    args.append([last, TOP])
    for _ in range(TILES - 1):
        args.append([rng.randint(0, TOP // 2), rng.randint(last + 1, TOP)])
    return {"ops": ["MyCalendarTwo"] + ["book"] * (len(args) - 1), "args": args}
