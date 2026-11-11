"""Array Statistics Tracker with ~5 * 10^4 calls: 2.5 * 10^4 numbers then adds, removals and
queries, or 4.4 * 10^4 distinct ascending numbers (all tied, so the first added is the mode) then
1.7 * 10^4 removals of that mode each followed by two getMode calls (~10^5 calls), so sorting for
each median or scanning the tied numbers for each mode costs ~10^9 steps."""

from _shapes import pick_shape

SEEDS = 3
CALLS = 5 * 10**4
FILL = 25000
TIED = 44000
ROUNDS = 17000


def generate(rng):
    ops, args = ["StatisticsTracker"], [[]]
    shape = pick_shape(rng)
    if shape == 2:
        for x in sorted(rng.sample(range(1, 10**5), TIED)):
            ops.append("addNumber")
            args.append([x])
        for _ in range(ROUNDS):
            ops += ["removeFirstAddedNumber", "getMode", "getMode"]
            args += [[], [], []]
            if rng.random() < 0.1:
                ops.append(rng.choice(("getMean", "getMedian")))
                args.append([])
        return {"ops": ops, "args": args}
    pool = [rng.randint(1, 10**6) for _ in range(500 if shape == 0 else 20000)]
    for _ in range(FILL):
        ops.append("addNumber")
        args.append([rng.choice(pool)])
    size = FILL
    for _ in range(CALLS - FILL):
        x = rng.random()
        if x < 0.15 or size == 1:
            ops.append("addNumber")
            args.append([rng.choice(pool)])
            size += 1
        elif x < 0.3:
            ops.append("removeFirstAddedNumber")
            args.append([])
            size -= 1
        else:
            ops.append(rng.choice(("getMean", "getMedian", "getMedian", "getMode")))
            args.append([])
    return {"ops": ops, "args": args}
