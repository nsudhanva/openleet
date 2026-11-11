"""Find Minimum Cost to Remove Array Elements at n = 200, so the three-way choice without
memoization is ~3^100 calls while the (kept element, position) DP is 2 * 10^4 states."""

SEEDS = 2
N = 200


def generate(rng):
    top = rng.choice((10**6, 10))
    return {"nums": [rng.randint(1, top) for _ in range(N)]}
