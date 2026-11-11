"""Maximum Capacity Within Budget at n = 7 * 10^4 with each capacity within 50 of its cost and a
budget near the cost range, so the best pairs sit at the budget edge and trying every pair is
~2.5 * 10^9 checks."""

SEEDS = 2
N = 7 * 10**4
LIMIT = 10**5


def generate(rng):
    costs = [rng.randint(1, LIMIT) for _ in range(N)]
    capacity = [max(1, min(LIMIT, c + rng.randint(-50, 50))) for c in costs]
    return {
        "costs": costs,
        "capacity": capacity,
        "budget": rng.randint(LIMIT * 4 // 5, LIMIT * 6 // 5),
    }
