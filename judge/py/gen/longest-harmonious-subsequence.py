"""Longest Harmonious Subsequence at the maximum n = 2 * 10^4 with almost every value distinct, so
counting each value's matches by a scan of the array does ~4 * 10^8 comparisons; one planted
pair of neighbouring values repeats to give the answer."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.5:
        # Distinct values spread over the whole range.
        nums = rng.sample(range(-LIMIT, LIMIT + 1), N)
    else:
        # Distinct even values: no neighbour pair at all apart from the planted one.
        nums = [2 * v for v in rng.sample(range(-LIMIT // 2, LIMIT // 2), N)]
    x = rng.randrange(-LIMIT, LIMIT)
    a, b = rng.randint(2, 40), rng.randint(2, 40)
    nums[: a + b] = [x] * a + [x + 1] * b
    rng.shuffle(nums)
    return {"nums": nums}
