"""MyQueue with the maximum 100 calls, interleaving pushes with peeks and pops only while the
queue is non-empty."""

SEEDS = 2


def generate(rng):
    ops, args, size = ["MyQueue"], [[]], 0
    for _ in range(100):
        r = rng.random()
        if size == 0 or r < 0.45:
            ops.append("push")
            args.append([rng.randint(1, 9)])
            size += 1
        elif r < 0.7:
            ops.append("pop")
            args.append([])
            size -= 1
        elif r < 0.85:
            ops.append("peek")
            args.append([])
        else:
            ops.append("empty")
            args.append([])
    return {"ops": ops, "args": args}
