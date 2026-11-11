"""Router with 36,000 calls: 18,000 packets, 95% to one destination, fill memory (with some
evictions and duplicates), then mostly getCount calls on that destination, so scanning the stored
packets per count (even per destination) costs ~3 * 10^8 steps."""

SEEDS = 2
CALLS = 36000
FILL = 18000
DESTS = 40
HOT = 0.95


def generate(rng):
    limit = rng.randint(FILL * 4 // 5, FILL)
    ops, args = ["Router"], [[limit]]
    t = 1
    last = None
    stored = []

    def dest():
        return 1 if rng.random() < HOT else rng.randint(2, DESTS)

    def add():
        nonlocal t, last
        if last and rng.random() < 0.05:
            ops.append("addPacket")
            args.append(list(last))
            return
        t += rng.randint(0, 3)
        last = (rng.randint(1, 1000), dest(), t)
        ops.append("addPacket")
        args.append(list(last))
        stored.append(t)

    for _ in range(FILL):
        add()
    for _ in range(CALLS - FILL):
        r = rng.random()
        if r < 0.9:
            a, b = sorted(rng.choice(stored) for _ in range(2))
            ops.append("getCount")
            args.append([dest(), a, b])
        elif r < 0.96:
            add()
        else:
            ops.append("forwardPacket")
            args.append([])
    return {"ops": ops, "args": args}
