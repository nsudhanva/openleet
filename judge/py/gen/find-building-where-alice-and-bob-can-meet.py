"""Find Building Where Alice and Bob Can Meet with 3 * 10^4 buildings and 3 * 10^4 queries: a tall
falling left half, then a rising staircase below it and a few tall buildings at the end, so scanning
right (or along next-greater links) from each query walks ~10^4 buildings, ~3 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
Q = 3 * 10**4
TOP = 10**9
TAIL = 50


def generate(rng):
    half = N // 2
    left = sorted(rng.sample(range(TOP // 2, TOP - TOP // 1000), half), reverse=True)
    stair = sorted(rng.sample(range(1, TOP // 2), N - half - TAIL))
    tail = [rng.randint(TOP // 2, TOP) for _ in range(TAIL)]
    queries = []
    for _ in range(Q):
        # Every query pairs a tall left building with a low early stair, in either order.
        a, b = rng.randrange(half), rng.randrange(half, half + max(1, len(stair) // 4))
        queries.append([a, b] if rng.random() < 0.5 else [b, a])
    return {"heights": left + stair + tail, "queries": queries}
