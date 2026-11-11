"""Rearranging Fruits at n = 2 * 10^4 per basket with ~10^4 distinct costs, every cost an even
total, so counting each cost by a scan costs ~4 * 10^8 comparisons."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    pool = [rng.randint(1, LIMIT) for _ in range(N // 2)]
    pool.append(rng.randint(1, 1000))
    half = [rng.choice(pool) for _ in range(N)]
    fruits = half + half
    rng.shuffle(fruits)
    return {"basket1": fruits[:N], "basket2": fruits[N:]}
