"""Count the Number of Good Subarrays at n = 2 * 10^4 over 2000 values with k reached only by
windows of about half the array, so extending each start until k pairs costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
VALUES = 2000


def generate(rng):
    pool = rng.sample(range(1, 10**9 + 1), VALUES)
    nums = [rng.choice(pool) for _ in range(N)]
    window = N // 2
    return {"nums": nums, "k": window * window // (2 * VALUES)}
