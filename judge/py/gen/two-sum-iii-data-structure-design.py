"""Two Sum III at 10^4 calls: 9,960 to 9,990 adds of distinct even numbers, then 10 to 40 finds,
mostly of odd values no pair reaches. Checking every pair per find is ~10^9 steps, and a design
that records every sum on add does ~5 * 10^7 set insertions against ~10^5 dictionary probes."""

from _shapes import pick_shape

SEEDS = 3
CALLS = 10**4
FINDS = (10, 20, 40)
TOP = 10**5


def generate(rng):
    finds = FINDS[pick_shape(rng)]
    adds = rng.sample(range(-TOP // 2, TOP // 2 + 1), CALLS - finds)
    ops, args = ["TwoSum"], [[]]
    for v in adds:
        ops.append("add")
        args.append([2 * v])
    for i in range(finds):
        if i % 5 == 2:
            # A reachable sum: two different values already added.
            a, b = rng.sample(adds, 2)
            target = 2 * (a + b)
        else:
            target = 2 * rng.randint(-TOP, TOP) + 1
        ops.append("find")
        args.append([target])
    return {"ops": ops, "args": args}
