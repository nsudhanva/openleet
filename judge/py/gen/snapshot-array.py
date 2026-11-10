"""Snapshot Array with length 5 * 10^4 and 5 * 10^4 calls: frequent snaps (copying the array per
snap is too slow) and gets on old snapshots of hot indices."""

SEEDS = 2
CALLS = 5 * 10**4


def generate(rng):
    length = 5 * 10**4
    ops, args = ["SnapshotArray", "snap"], [[length], []]
    snaps = 1
    hot = [rng.randrange(length) for _ in range(20)]
    snap_rate = rng.choice([0.3, 0.05])
    for _ in range(CALLS - 1):
        r = rng.random()
        idx = rng.choice(hot) if rng.random() < 0.7 else rng.randrange(length)
        if r < snap_rate:
            ops.append("snap")
            args.append([])
            snaps += 1
        elif r < snap_rate + (1 - snap_rate) / 2:
            ops.append("set")
            args.append([idx, rng.randint(0, 10**9)])
        else:
            ops.append("get")
            args.append([idx, rng.randrange(snaps)])
    return {"ops": ops, "args": args}
