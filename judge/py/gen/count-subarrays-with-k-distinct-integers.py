"""Count Subarrays With K Distinct Integers at n = 2 * 10^4 drawn from exactly k <= 4 values, or
n = 5 * 10^4 in runs of m to m + 2 equal values with k in the thousands, so extending every start
until it passes k distinct costs 10^8+ steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
BLOCKS_N = 5 * 10**4
LIMIT = 10**5
POOL = 2500


def blocks(rng, m, values):
    nums, i = [], 0
    while len(nums) < BLOCKS_N:
        nums += [values[i % len(values)]] * rng.randint(m, m + 2)
        i += 1
    return nums[:BLOCKS_N]


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        k = rng.randint(2, 4)
        values = rng.sample(range(1, LIMIT + 1), k)
        nums = [rng.choice(values) for _ in range(N)]
        return {"nums": nums, "k": k, "m": rng.randint(N // 50, N // 10)}
    if shape == 1:
        return {"nums": blocks(rng, 2, range(1, LIMIT + 1)), "k": BLOCKS_N // 25, "m": 2}
    values = rng.sample(range(1, LIMIT + 1), POOL)
    return {"nums": blocks(rng, 3, values), "k": POOL * 2 // 5, "m": 3}
