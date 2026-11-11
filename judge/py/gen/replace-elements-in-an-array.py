"""Replace Elements in an Array at n = m = 2 * 10^4 with every operation renaming an element near
the end, so locating each by a scan costs ~4 * 10^8 comparisons."""

SEEDS = 2
N = 2 * 10**4
M = 2 * 10**4


def generate(rng):
    values = rng.sample(range(1, 10**6 + 1), N + M)
    nums = values[:N]
    current = nums[:]
    tail = rng.choice((1, N // 20))
    operations = []
    for y in values[N:]:
        i = N - 1 - rng.randrange(tail)
        operations.append([current[i], y])
        current[i] = y
    return {"nums": nums, "operations": operations}
