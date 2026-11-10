"""Number of Longest Increasing Subsequence at n = 2000: random values, or rising blocks of
decreasing runs so the count multiplies up; every input is checked to keep the count within
32 bits."""

SEEDS = 3
N = 2000
LIMIT = 10**6
CAP = 2**31 - 1


def lis_count(nums):
    """Number of longest strictly increasing subsequences, via a Fenwick tree of (len, count)."""
    order = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    size = len(order)
    best = [(0, 0)] * (size + 1)

    def merge(a, b):
        if a[0] != b[0]:
            return a if a[0] > b[0] else b
        return (a[0], a[1] + b[1])

    for v in nums:
        i, got = order[v] - 1, (0, 1)
        while i > 0:
            got = merge(got, best[i]) if best[i][0] else got
            i -= i & -i
        here = (got[0] + 1, got[1]) if got[0] else (1, 1)
        i = order[v]
        while i <= size:
            best[i] = merge(best[i], here)
            i += i & -i
    total = (0, 0)
    i = size
    while i > 0:
        total = merge(total, best[i])
        i -= i & -i
    return total[1]


def generate(rng):
    while True:
        if rng.random() < 0.5:
            nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
        else:
            threes = rng.randint(0, 19)
            twos = rng.randint(0, (CAP // 3**threes).bit_length() - 1)
            sizes = [3] * threes + [2] * twos
            sizes += [1] * (N - sum(sizes))
            rng.shuffle(sizes)
            nums, base = [], -LIMIT
            for size in sizes:
                nums.extend(range(base + size - 1, base - 1, -1))
                base += size
        if lis_count(nums) <= CAP:
            return {"nums": nums}
