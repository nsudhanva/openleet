"""Maximum Coins From K Consecutive Bags with 10^4 unsorted non-overlapping segments over
[1, 10^9] and k about a third of the span, so summing every candidate window over all segments
is 2 * 10^8 steps."""

SEEDS = 2
N = 10**4
SPAN = 10**9


def generate(rng):
    ends = sorted(rng.sample(range(1, SPAN + 1), 2 * N))
    coins = [[ends[2 * i], ends[2 * i + 1], rng.randint(1, 1000)] for i in range(N)]
    rng.shuffle(coins)
    return {"coins": coins, "k": rng.randint(SPAN // 4, SPAN // 2)}
