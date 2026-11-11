"""Sum of GCD of Formed Pairs at n = 5 * 10^4 values sharing small factors, so taking the maximum of
every prefix afresh is ~1.2 * 10^9 steps."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    nums = []
    for _ in range(N):
        f = rng.choice((1, 2, 6, 12, 30, 210, 2310))
        nums.append(f * rng.randint(1, 10**9 // f))
    return {"nums": nums}
