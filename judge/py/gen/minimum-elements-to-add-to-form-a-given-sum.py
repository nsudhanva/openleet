"""Minimum Elements to Add to Form a Given Sum with 1000 values, limit <= 3 and |goal| near
10^9: adding one element of size limit at a time takes ~3 * 10^8 steps."""

SEEDS = 2
N = 1000
GOAL = 10**9


def generate(rng):
    limit = rng.randint(1, 3)
    nums = [rng.randint(-limit, limit) for _ in range(N)]
    goal = rng.choice((-1, 1)) * rng.randint(GOAL - 1000, GOAL)
    return {"nums": nums, "limit": limit, "goal": goal}
