"""Design Circular Deque with 2000 calls on a capacity of up to 1000, wrapping both ends
around the buffer many times (including operations on a full or empty deque)."""

SEEDS = 2
CALLS = 2000
METHODS = ["insertFront", "insertLast", "deleteLast", "getFront", "getRear", "isFull"]


def generate(rng):
    k = rng.choice([1, rng.randint(2, 50), 1000])
    ops, args = ["MyCircularDeque"], [[k]]
    for _ in range(CALLS):
        op = rng.choices(METHODS, weights=[3, 3, 3, 1, 1, 1])[0]
        ops.append(op)
        args.append([rng.randint(0, 1000)] if op.startswith("insert") else [])
    return {"ops": ops, "args": args}
