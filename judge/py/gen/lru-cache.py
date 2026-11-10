"""LRU Cache with 2 * 10^5 calls: small capacity so evictions happen constantly."""

SEEDS = 2
CALLS = 2 * 10**5


def generate(rng):
    capacity = rng.randint(1, 3000)
    ops, args = ["LRUCache"], [[capacity]]
    for _ in range(CALLS):
        key = rng.randint(0, 10**4)
        if rng.random() < 0.5:
            ops.append("put")
            args.append([key, rng.randint(0, 10**5)])
        else:
            ops.append("get")
            args.append([key])
    return {"ops": ops, "args": args}
