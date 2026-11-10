"""Min Stack with 3 * 10^4 calls: mostly pushes of decreasing values so getMin changes
constantly, with pops, tops and getMins only on a non-empty stack."""

SEEDS = 3
CALLS = 3 * 10**4
LOW, HIGH = -(2**31), 2**31 - 1


def generate(rng):
    ops, args = ["MinStack"], [[]]
    size = 0
    descending = rng.random() < 0.5
    value = HIGH
    for _ in range(CALLS):
        roll = rng.random()
        if size == 0 or roll < 0.45:
            if descending:
                value = max(LOW, value - rng.randint(0, 2**18))
                v = value
            else:
                v = rng.randint(LOW, HIGH)
            ops.append("push")
            args.append([v])
            size += 1
        elif roll < 0.65:
            ops.append("pop")
            args.append([])
            size -= 1
        elif roll < 0.8:
            ops.append("top")
            args.append([])
        else:
            ops.append("getMin")
            args.append([])
    return {"ops": ops, "args": args}
