"""Closest Equal Element Queries at n = q = 10^5: one value fills every even index and the odd
indices hold random pairs about n / 4 apart (a few odd ones once), so an outward scan per query
costs ~10^9 steps and searching the big value's position list ~10^9 more."""

SEEDS = 2
N = 10**5
SINGLE = 500


def generate(rng):
    nums = [1] * N
    odd = list(range(1, N, 2))
    rng.shuffle(odd)
    values = rng.sample(range(2, 10**5), len(odd))
    for i in odd[:SINGLE]:
        nums[i] = values.pop()
    rest = odd[SINGLE:]
    for a, b in zip(rest[::2], rest[1::2], strict=False):
        nums[a] = nums[b] = values.pop()
    if len(rest) % 2:
        nums[rest[-1]] = values.pop()
    return {"nums": nums, "queries": [rng.randrange(N) for _ in range(N)]}
