"""Count the Number of Fair Pairs at n = 10^5 in descending order (each insertion into a sorted
list lands at the front), so checking every pair costs 5 * 10^9 tests."""

SEEDS = 2
N = 10**5
LIMIT = 5 * 10**6


def generate(rng):
    nums = sorted((rng.randint(-LIMIT, LIMIT) for _ in range(N)), reverse=True)
    upper = rng.randint(-LIMIT // 2, LIMIT // 2)
    return {"nums": nums, "lower": -(10**9), "upper": upper}
