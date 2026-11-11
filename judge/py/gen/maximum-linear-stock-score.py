"""Maximum Linear Stock Score at n = 2 * 10^4 where every price is its day plus one of n/4
offsets, so the quadratic DP over earlier days is 2 * 10^8 steps and summing each offset's group
by a full scan 10^8."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    offsets = rng.sample(range(1, LIMIT - N), N // 4)
    return {"prices": [i + rng.choice(offsets) for i in range(N)]}
