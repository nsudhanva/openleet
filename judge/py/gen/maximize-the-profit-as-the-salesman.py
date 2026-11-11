"""Maximize the Profit as the Salesman with 3 * 10^4 offers over 10^5 houses, each spanning a
random third of the line, so a quadratic DP over earlier offers does ~4.5 * 10^8 checks."""

SEEDS = 2
N = 10**5
M = 3 * 10**4


def generate(rng):
    offers = []
    for _ in range(M):
        length = rng.randint(N // 6, N // 2)
        start = rng.randrange(N - length)
        offers.append([start, start + length, rng.randint(1, 1000)])
    return {"n": N, "offers": offers}
