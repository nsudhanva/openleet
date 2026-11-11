"""Maximum Earnings From Taxi with 3 * 10^4 rides (the maximum) over 10^5 points, each spanning
up to a third of the road, so the quadratic DP over every earlier ride is 4.5 * 10^8 checks."""

SEEDS = 2
N = 10**5
M = 3 * 10**4


def generate(rng):
    rides = []
    for _ in range(M):
        length = rng.randint(1, N // 3)
        start = rng.randint(1, N - length)
        rides.append([start, start + length, rng.randint(1, 10**5)])
    return {"n": N, "rides": rides}
