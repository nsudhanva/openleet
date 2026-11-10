"""Minimum Number of Days to Make m Bouquets at n = 10^5 with bloom days up to 10^9: m * k
just fits (or just fails), so day-by-day simulation is hopeless."""

SEEDS = 3
N = 10**5


def generate(rng):
    bloom = [rng.randint(1, 10**9) for _ in range(N)]
    k = rng.choice((1, 3, 100, rng.randint(1, N)))
    most = N // k
    m = rng.choice((most, most + 1, max(1, most // 2)))
    return {"bloomDay": bloom, "m": min(m, 10**6), "k": k}
