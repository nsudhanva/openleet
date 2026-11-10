"""MedianFinder with 5 * 10^4 calls: adds in random, ascending, or descending order, with
findMedian interleaved throughout."""

SEEDS = 3
CALLS = 5 * 10**4


def generate(rng):
    shape = rng.randrange(3)
    adds = CALLS * 2 // 3
    if shape == 0:
        values = [rng.randint(-(10**5), 10**5) for _ in range(adds)]
    else:
        values = sorted(rng.randint(-(10**5), 10**5) for _ in range(adds))
        if shape == 2:
            values.reverse()
    ops, args = ["MedianFinder", "addNum"], [[], [values[0]]]
    i, calls = 1, 1
    while calls < CALLS:
        if i < adds and rng.random() < 0.67:
            ops.append("addNum")
            args.append([values[i]])
            i += 1
        else:
            ops.append("findMedian")
            args.append([])
        calls += 1
    return {"ops": ops, "args": args}
