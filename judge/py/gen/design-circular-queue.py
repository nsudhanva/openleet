"""Design Circular Queue with 3000 calls on a capacity of up to 1000, wrapping around the
buffer many times (including operations on a full or empty queue)."""

SEEDS = 2
CALLS = 3000
METHODS = ["enQueue", "deQueue", "Rear", "isFull"]


def generate(rng):
    k = rng.choice([1, rng.randint(2, 50), 1000])
    ops, args = ["MyCircularQueue"], [[k]]
    for _ in range(CALLS):
        op = rng.choices(METHODS, weights=[4, 3, 1, 1])[0]
        ops.append(op)
        args.append([rng.randint(0, 1000)] if op == "enQueue" else [])
    return {"ops": ops, "args": args}
