"""Stock Price Fluctuation with 10^5 calls: many corrections to old timestamps (stale heap
entries) and frequent max/min/current queries."""

SEEDS = 2
CALLS = 10**5


def generate(rng):
    ops, args = ["StockPrice"], [[]]
    span = rng.choice([50, 10**4])
    ops.append("update")
    args.append([rng.randint(1, span), rng.randint(1, 10**9)])
    for _ in range(CALLS - 1):
        r = rng.random()
        if r < 0.55:
            ops.append("update")
            args.append([rng.randint(1, span), rng.randint(1, 10**9)])
        else:
            ops.append(rng.choice(["current", "maximum", "minimum"]))
            args.append([])
    return {"ops": ops, "args": args}
