"""Data Stream as Disjoint Intervals with 3 * 10^4 calls (100 of them getIntervals): values
spread over [0, 10^4] so intervals keep merging, or only even values so thousands of
disjoint intervals must be returned."""

SEEDS = 2
CALLS = 3 * 10**4
GETS = 100


def generate(rng):
    evens = rng.random() < 0.5
    ops, args = ["SummaryRanges"], [[]]
    gets = set(rng.sample(range(CALLS), GETS))
    for i in range(CALLS):
        if i in gets:
            ops.append("getIntervals")
            args.append([])
        else:
            v = 2 * rng.randint(0, 5000) if evens else rng.randint(0, 10**4)
            ops.append("addNum")
            args.append([v])
    return {"ops": ops, "args": args}
