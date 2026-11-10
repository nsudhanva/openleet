"""LFU Cache with 2 * 10^5 calls over a small key range, so frequency ties and evictions
happen constantly."""

SEEDS = 2
CALLS = 2 * 10**5


def generate(rng):
    capacity = rng.choice([1, rng.randint(2, 100), rng.randint(1000, 10**4)])
    keys = rng.randint(capacity + 1, max(capacity + 2, 3 * capacity))
    keys = min(keys, 10**5)
    ops, args = ["LFUCache"], [[capacity]]
    for _ in range(CALLS):
        key = rng.randint(0, keys)
        if rng.random() < 0.5:
            ops.append("put")
            args.append([key, rng.randint(0, 10**9)])
        else:
            ops.append("get")
            args.append([key])
    return {"ops": ops, "args": args}
