"""Maximum Frequency Stack with 2 * 10^4 calls: pushes over a few values build high
frequencies, and pops only when the stack is non-empty."""

SEEDS = 2
CALLS = 2 * 10**4


def generate(rng):
    pool = [rng.randint(0, 10**9) for _ in range(rng.choice([3, 50, 1000]))]
    ops, args = ["FreqStack"], [[]]
    size = 0
    push_rate = rng.choice([0.6, 0.75])
    for _ in range(CALLS):
        if size == 0 or rng.random() < push_rate:
            ops.append("push")
            args.append([rng.choice(pool)])
            size += 1
        else:
            ops.append("pop")
            args.append([])
            size -= 1
    return {"ops": ops, "args": args}
