"""Design Skiplist with 3 * 10^4 calls: 1.5 * 10^4 adds, then searches, adds and erases of
mostly large values, so walking a plain sorted linked list is ~10^8 steps."""

SEEDS = 2
CALLS = 3 * 10**4
TOP = 2 * 10**4


def generate(rng):
    ops, args = ["Skiplist"], [[]]
    added = []
    for _ in range(CALLS // 2):
        added.append(rng.randint(0, TOP))
        ops.append("add")
        args.append([added[-1]])
    while len(ops) <= CALLS:
        r = rng.random()
        if rng.random() < 0.5:
            num = rng.choice(added)
        else:
            num = TOP - int(rng.expovariate(1 / 2000)) % TOP
        ops.append("search" if r < 0.5 else "add" if r < 0.75 else "erase")
        args.append([num])
        if ops[-1] == "add":
            added.append(num)
    return {"ops": ops, "args": args}
