"""Kth Largest in a Stream with 10^4 initial numbers and 10^4 adds; sorting on every add is
quadratic."""

SEEDS = 2
N = 10**4
CALLS = 10**4
LIMIT = 10**4


def generate(rng):
    nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    k = rng.choice([1, N // 2, N + 1, rng.randint(1, N + 1)])
    ops, args = ["KthLargest"], [[k, nums]]
    ascending = rng.random() < 0.5
    for i in range(CALLS):
        val = -LIMIT + 2 * LIMIT * i // CALLS if ascending else rng.randint(-LIMIT, LIMIT)
        ops.append("add")
        args.append([val])
    return {"ops": ops, "args": args}
