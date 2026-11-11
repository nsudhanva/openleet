"""Count Integers in Intervals with 4 * 10^4 calls alternating add and count, intervals of at most
10^4 integers scattered over [1, 10^9] so few of them merge, so re-merging every interval on each
count costs ~4 * 10^8 steps and marking integers one by one far more."""

SEEDS = 2
CALLS = 4 * 10**4
LIMIT = 10**9
LONGEST = 10**4


def generate(rng):
    ops, args = ["CountIntervals"], [[]]
    for i in range(CALLS):
        if i % 2 == 0:
            left = rng.randint(1, LIMIT)
            right = min(LIMIT, left + rng.randint(0, LONGEST))
            ops.append("add")
            args.append([left, right])
        else:
            ops.append("count")
            args.append([])
    return {"ops": ops, "args": args}
