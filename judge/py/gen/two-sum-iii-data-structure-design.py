"""Two Sum III at 1300 calls: 1000 adds of distinct even numbers, then 300 finds of odd values
no pair reaches, so checking every pair per find is ~1.5 * 10^8 steps."""

SEEDS = 2
ADDS = 1000
FINDS = 300
TOP = 10**5


def generate(rng):
    ops, args = ["TwoSum"], [[]]
    for v in rng.sample(range(-TOP // 2, TOP // 2 + 1), ADDS):
        ops.append("add")
        args.append([2 * v])
    for _ in range(FINDS):
        ops.append("find")
        args.append([2 * rng.randint(-TOP, TOP) + 1])
    return {"ops": ops, "args": args}
