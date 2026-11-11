"""Maximum Ice Cream Bars at n = 2 * 10^4 with coins for all but a few bars, so picking the
cheapest remaining bar by a scan each time is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
COST = 10**4


def generate(rng):
    costs = [rng.randint(1, COST) for _ in range(N)]
    cheapest = sorted(costs)
    coins = min(10**8, sum(cheapest[: N - rng.randint(1, 10)]))
    return {"costs": costs, "coins": max(1, coins)}
