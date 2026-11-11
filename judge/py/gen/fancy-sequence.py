"""Fancy Sequence with 6.5 * 10^4 calls: 2 * 10^4 appends, 1.5 * 10^4 updates, then 1.5 * 10^4
(update, getIndex) pairs each on a value untouched since the start, so applying updates to every
value (or replaying the missed ones at each get) is ~3 * 10^8 steps or more."""

SEEDS = 2
APPENDS = 2 * 10**4
UPDATES = 15 * 10**3
GETS = 15 * 10**3


def generate(rng):
    ops, args = ["Fancy"], [[]]

    def update():
        ops.append("addAll" if rng.random() < 0.5 else "multAll")
        args.append([rng.randint(1, 100)])

    for _ in range(APPENDS):
        ops.append("append")
        args.append([rng.randint(1, 100)])
    for _ in range(UPDATES):
        update()
    # An update before every get forces a pending-update flush; each get asks for a fresh index.
    for idx in rng.sample(range(APPENDS), GETS):
        update()
        ops.append("getIndex")
        args.append([idx])
    return {"ops": ops, "args": args}
