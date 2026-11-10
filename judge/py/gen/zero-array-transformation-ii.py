"""Zero Array Transformation II at 10^5 numbers and 10^5 queries: the answer lands near the
last query (punishing a linear scan with full re-application), or never (-1)."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    queries = []
    for _ in range(N):
        left = rng.randrange(N)
        right = rng.randrange(left, min(N, left + rng.choice([10, 1000, N])))
        queries.append([left, right, rng.randint(1, 5)])
    # Coverage per index if every query is used.
    diff = [0] * (N + 1)
    for left, right, val in queries:
        diff[left] += val
        diff[right + 1] -= val
    cover, run = [], 0
    for i in range(N):
        run += diff[i]
        cover.append(run)
    if shape == 0:
        nums = [min(5 * 10**5, c) for c in cover]  # tight: needs (nearly) all queries
    elif shape == 1:
        nums = [rng.randint(0, min(5 * 10**5, c)) for c in cover]
    else:
        nums = [min(5 * 10**5, c) for c in cover]
        i = rng.randrange(N)
        if nums[i] < 5 * 10**5:
            nums[i] += 1  # one index can never reach zero
    return {"nums": nums, "queries": queries}
