"""Number of Subsequences That Satisfy the Given Sum Condition at 2 * 10^4 values with a target that
nearly every pair meets, so scanning for each minimum's furthest partner costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**6


def generate(rng):
    nums = [rng.randint(1, TOP // 2) for _ in range(N)]
    target = rng.randint(TOP * 9 // 10, TOP)
    return {"nums": nums, "target": target}
