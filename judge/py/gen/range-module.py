"""Range Module with 10^4 mixed calls over a narrow coordinate span, so ranges overlap, merge
and split constantly."""

SEEDS = 2
CALLS = 10**4


def generate(rng):
    span = rng.choice([10**4, 10**9])
    width = max(2, span // 50)
    ops, args = ["RangeModule"], [[]]
    for _ in range(CALLS):
        left = rng.randint(1, span - 1)
        right = min(span, left + rng.randint(1, width))
        ops.append(rng.choice(["addRange", "addRange", "removeRange", "queryRange"]))
        args.append([left, right])
    return {"ops": ops, "args": args}
