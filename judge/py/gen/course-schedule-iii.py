"""Course Schedule III with 10^4 courses of 1 to 3 days, all due in the last thousand of the 10^4
days: the greedy swaps half of them out through its heap, and a day-by-day DP does ~10^8 steps."""

SEEDS = 2
N = 10**4
DAYS = 10**4


def generate(rng):
    courses = [[rng.randint(1, 3), rng.randint(DAYS - 1000, DAYS)] for _ in range(N)]
    return {"courses": courses}
