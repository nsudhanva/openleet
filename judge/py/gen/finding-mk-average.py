"""4 * 10^4 calls with m of 5000 to 10^4: m adds fill the window, then adds and averages
alternate, so re-sorting the window for each of the ~1.5 * 10^4 averages handles ~10^8 values."""

SEEDS = 2
CALLS = 4 * 10**4


def generate(rng):
    m = rng.randint(5000, 10**4)
    k = rng.randint(1, (m - 1) // 2)
    ops, args = ["MKAverage"], [[m, k]]
    for i in range(CALLS):
        if i < m or i % 2:
            ops.append("addElement")
            args.append([rng.randint(1, 10**5)])
        else:
            ops.append("calculateMKAverage")
            args.append([])
    return {"ops": ops, "args": args}
