"""Number of Subsequences That Satisfy the Given Sum Condition. Seed 0: 2 * 10^4 values with a
target that nearly every pair meets, so scanning up from each minimum for its furthest partner
costs ~2 * 10^8 steps. Seed 1: 3 * 10^4 values, half tiny and half huge, with a target that every
tiny-tiny pair meets and no huge value does, so scanning down from the end past all the huge values
for each tiny minimum costs ~2 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 2
N = 2 * 10**4
N_SPLIT = 3 * 10**4
TOP = 10**6


def generate(rng):
    if pick_shape(rng) == 2:
        half = N_SPLIT // 2
        nums = [rng.randint(1, 1000) for _ in range(half)]
        nums += [rng.randint(TOP * 9 // 10, TOP) for _ in range(half)]
        rng.shuffle(nums)
        return {"nums": nums, "target": rng.randint(TOP // 2, TOP * 8 // 10)}
    nums = [rng.randint(1, TOP // 2) for _ in range(N)]
    target = rng.randint(TOP * 9 // 10, TOP)
    return {"nums": nums, "target": target}
