"""Count of Interesting Subarrays at n = 2 * 10^4 with a small modulo, so recounting every
subarray costs 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    modulo = rng.randint(2, 5)
    k = rng.randrange(modulo)
    return {"nums": [rng.randint(1, LIMIT) for _ in range(N)], "modulo": modulo, "k": k}
