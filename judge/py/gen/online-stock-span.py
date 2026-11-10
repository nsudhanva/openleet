"""Online Stock Span with 10^4 calls: non-increasing prices then a spike, or slowly rising
prices so spans are long and a backward scan is quadratic."""

SEEDS = 2
CALLS = 10**4


def generate(rng):
    if rng.random() < 0.5:
        prices = sorted((rng.randint(1, 10**5) for _ in range(CALLS)), reverse=True)
        prices[-1] = 10**5
    else:
        prices = sorted(rng.randint(1, 10**5) for _ in range(CALLS))
    ops, args = ["StockSpanner"], [[]]
    for p in prices:
        ops.append("next")
        args.append([p])
    return {"ops": ops, "args": args}
