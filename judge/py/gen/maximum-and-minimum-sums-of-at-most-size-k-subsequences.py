"""Maximum and Minimum Sums of at Most Size K Subsequences at n = 2 * 10^4 drawn from a pool of
n values (about 1.3 * 10^4 distinct, the rest repeats), so ranking each value against all the
others is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    pool = [rng.randint(0, LIMIT) for _ in range(N)]
    return {"nums": [rng.choice(pool) for _ in range(N)], "k": rng.randint(5, 20)}
