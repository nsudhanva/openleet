"""Apply Operations to Maximize Frequency Score at n = 3 * 10^4 with k set so the best window
holds about half the array, so growing a window from every start is ~4 * 10^8 steps."""

from itertools import accumulate

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    top = rng.choice([10**9, 10**6])
    nums = [rng.randint(1, top) for _ in range(N)]
    s = sorted(nums)
    pre = list(accumulate(s, initial=0))
    size = N // 2
    costs = []
    for i in range(N - size + 1):
        j, m = i + size, i + size // 2
        costs.append(s[m] * (m - i) - (pre[m] - pre[i]) + (pre[j] - pre[m]) - s[m] * (j - m))
    costs.sort()
    return {"nums": nums, "k": costs[len(costs) // 2]}
