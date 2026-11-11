"""Time to Cross a Bridge at n = k = 10^4, so picking the least efficient waiting worker and the
next one to finish by scanning every worker is ~2 * 10^8 steps."""

SEEDS = 2
N = 10**4
K = 10**4


def generate(rng):
    hi = rng.choice((1000, 50))
    time = [[rng.randint(1, hi) for _ in range(4)] for _ in range(K)]
    return {"n": N, "k": K, "time": time}
