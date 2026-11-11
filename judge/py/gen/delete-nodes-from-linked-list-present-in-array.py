"""Delete Nodes From Linked List Present in an Array with 5 * 10^4 distinct nums and a 5 * 10^4
node list mostly of other values, so testing membership by scanning nums costs ~2.5 * 10^9
comparisons."""

SEEDS = 2
N = 5 * 10**4
TOP = 10**5


def generate(rng):
    values = rng.sample(range(1, TOP + 1), TOP)
    nums, others = values[:N], values[N:]
    head = [rng.choice(nums) if rng.random() < 0.1 else rng.choice(others) for _ in range(N)]
    head[rng.randrange(N)] = rng.choice(others)
    return {"nums": nums, "head": head}
