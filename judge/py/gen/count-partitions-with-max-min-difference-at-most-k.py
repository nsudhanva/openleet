"""Count Partitions With Max-Min Difference at Most K at n = 2 * 10^4 on a slow random walk
whose valid segments run to thousands of elements, so scanning back from every cut costs
~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    step = LIMIT // (4 * N)
    x, nums = LIMIT // 2, []
    for _ in range(N):
        x = min(LIMIT, max(1, x + rng.randint(-step, step)))
        nums.append(x)
    k = step * 60
    return {"nums": nums, "k": k}
