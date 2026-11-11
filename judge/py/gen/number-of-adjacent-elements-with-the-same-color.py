"""Number of Adjacent Elements With the Same Color at n = 2 * 10^4 and 2 * 10^4 queries with
three colours (so many neighbours match and get repainted), so recounting the whole array after
each query is ~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    queries = [[rng.randrange(N), rng.randint(1, 3)] for _ in range(N)]
    return {"n": N, "queries": queries}
