"""Replace Elements in an Array at n = m = 5 * 10^4 with operations alternately renaming an element
within the last and within the first few of the array, so locating each by a scan from either end
costs ~1.25 * 10^9 comparisons."""

SEEDS = 2
N = 5 * 10**4
M = 5 * 10**4


def generate(rng):
    values = rng.sample(range(1, 10**6 + 1), N + M)
    nums = values[:N]
    current = nums[:]
    tail = rng.choice((1, N // 20))
    operations = []
    for k, y in enumerate(values[N:]):
        i = rng.randrange(tail) if k % 2 else N - 1 - rng.randrange(tail)
        operations.append([current[i], y])
        current[i] = y
    return {"nums": nums, "operations": operations}
