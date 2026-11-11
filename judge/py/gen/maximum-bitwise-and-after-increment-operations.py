"""Maximum Bitwise AND After Increment Operations at n = 10^4 with m around half of n, so choosing
the m cheapest numbers by repeated scans for every bit is ~10^9 steps."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    return {
        "nums": [rng.randint(1, LIMIT) for _ in range(N)],
        "k": rng.randint(LIMIT // 2, LIMIT),
        "m": rng.randint(N // 4, 3 * N // 4),
    }
