"""Count Special Subsequences at n = 1000 values with no prime factor above 5 (many equal
ratios), so fixing p, q and r and looking up s costs ~1.7 * 10^8 steps."""

SEEDS = 2
N = 1000
LIMIT = 1000


def smooth(v):
    for p in (2, 3, 5):
        while v % p == 0:
            v //= p
    return v == 1


def generate(rng):
    pool = [v for v in range(1, LIMIT + 1) if smooth(v)]
    pool = rng.sample(pool, min(len(pool), rng.randint(20, 60)))
    return {"nums": [rng.choice(pool) for _ in range(N)]}
