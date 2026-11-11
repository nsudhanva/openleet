"""Append K Integers With Minimal Sum at n = 10^4 and k = 10^8, values spread over the range
the answer covers, so trying candidates one by one takes ~10^8 steps."""

SEEDS = 2
N = 10**4
K = 10**8


def generate(rng):
    top = rng.choice([K + K // 10, 2 * K])
    return {"nums": [rng.randint(1, top) for _ in range(N)], "k": K}
