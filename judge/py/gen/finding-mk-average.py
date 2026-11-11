"""10^5 calls with m of 25000 to 30000 and k of 1 to 10: m adds fill the window, then 80% of the
calls are averages with a few adds between, so re-sorting the window or summing its middle
slice for each of the ~6 * 10^4 averages touches ~1.8 * 10^9 values."""

SEEDS = 2
CALLS = 10**5
ADD_SHARE = 0.2
WINDOW = (25000, 30000)


def generate(rng):
    m = rng.randint(*WINDOW)
    k = rng.randint(1, 10)
    ops, args = ["MKAverage"], [[m, k]]
    for i in range(CALLS):
        if i < m or rng.random() < ADD_SHARE:
            ops.append("addElement")
            args.append([rng.randint(1, 10**5)])
        else:
            ops.append("calculateMKAverage")
            args.append([])
    return {"ops": ops, "args": args}
