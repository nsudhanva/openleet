"""Maximum Number of Groups Getting Fresh Donuts with batchSize 9 and 30 groups whose remainders
are all in 1..4, so no two groups pair off and a DP over subsets of groups (2^30 states) cannot
finish."""

SEEDS = 2
BATCH = 9
N = 30


def generate(rng):
    groups = [rng.randrange(10**9 // BATCH) * BATCH + rng.choice((1, 2, 3, 4)) for _ in range(N)]
    return {"batchSize": BATCH, "groups": groups}
