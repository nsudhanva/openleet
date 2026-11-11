"""Moving Stones Until Consecutive II at n = 10^4 stones packed into a span of ~1.2n at a random
offset, so counting the stones in each length-n window by a fresh scan is ~8 * 10^7 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    base = rng.randint(1, 10**9 - 2 * N)
    stones = rng.sample(range(base, base + N * 6 // 5), N)
    return {"stones": stones}
