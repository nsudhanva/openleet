"""Best Sightseeing Pair at n = 5 * 10^4: random values, or decreasing values where the best
pair is adjacent and a quadratic scan checks every pair."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        values = [rng.randint(1, 1000) for _ in range(N)]
    else:
        values = [max(1, 1000 - i // 50) for i in range(N)]
    return {"values": values}
