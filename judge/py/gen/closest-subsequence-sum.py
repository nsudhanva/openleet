"""Closest Subsequence Sum at n = 34 with spread-out even values and an odd goal in the middle of
the reachable range, so no subset hits it and no search can stop early: 2^34 subset sums."""

SEEDS = 2
N = 34
LIMIT = 10**7


def generate(rng):
    nums = [2 * rng.randint(-LIMIT // 2, LIMIT // 2) for _ in range(N)]
    top = sum(x for x in nums if x > 0)
    low = sum(x for x in nums if x < 0)
    goal = 2 * rng.randint(low // 4, top // 4) + 1
    return {"nums": nums, "goal": goal}
