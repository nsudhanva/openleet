"""Design Linked List with 2000 calls growing the list to hundreds of nodes, with indexed
inserts, deletes and gets deep in the list (plus some out-of-range indices)."""

SEEDS = 2
CALLS = 2000


def generate(rng):
    size = 0
    ops, args = ["MyLinkedList"], [[]]
    for _ in range(CALLS):
        x = rng.random()
        val = rng.randint(0, 1000)
        if x < 0.2:
            ops.append("addAtHead")
            args.append([val])
            size += 1
        elif x < 0.4:
            ops.append("addAtTail")
            args.append([val])
            size += 1
        elif x < 0.6:
            index = rng.randint(0, min(1000, size + 2))
            ops.append("addAtIndex")
            args.append([index, val])
            if index <= size:
                size += 1
        elif x < 0.7:
            index = rng.randint(0, min(1000, size + 2))
            ops.append("deleteAtIndex")
            args.append([index])
            if index < size:
                size -= 1
        else:
            ops.append("get")
            args.append([rng.randint(0, min(1000, size + 2))])
    return {"ops": ops, "args": args}
