"""Product of the Last K Numbers at the maximum 4 * 10^4 calls: 2 * 10^4 adds (mostly 1s, a few
2s and 3s, one 0 near the start) then 2 * 10^4 getProduct calls over nearly the whole stream, so
multiplying the last k numbers per query does ~4 * 10^8 steps."""

SEEDS = 2
CALLS = 4 * 10**4
ADDS = 2 * 10**4
SPREAD = 100


def generate(rng):
    nums = [1] * ADDS
    for i in rng.sample(range(SPREAD, ADDS), 20):
        nums[i] = 2
    for i in rng.sample(range(SPREAD, ADDS), 3):
        nums[i] = 3
    # Windows start at indices 0..SPREAD - 1, so about half of them cover the 0.
    nums[rng.randrange(SPREAD * 3 // 10, SPREAD * 7 // 10)] = 0
    ops, args = ["ProductOfNumbers"], [[]]
    for x in nums:
        ops.append("add")
        args.append([x])
    while len(ops) - 1 < CALLS:
        ops.append("getProduct")
        args.append([ADDS - rng.randrange(SPREAD)])
    return {"ops": ops, "args": args}
