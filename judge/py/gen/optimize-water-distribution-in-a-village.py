"""Optimize Water Distribution in a Village at the maximum 10^4 houses and 10^4 pipes, so a Prim
that scans every house for the cheapest one to add costs 10^8 steps."""

SEEDS = 2
N = 10**4
TOP = 10**5


def generate(rng):
    wells = [
        rng.randint(TOP // 2, TOP) if rng.random() < 0.9 else rng.randint(0, TOP) for _ in range(N)
    ]
    pipes = []
    for _ in range(N):
        a = rng.randint(1, N)
        b = rng.randint(1, N - 1)
        b += b >= a
        pipes.append([a, b, rng.randint(0, TOP // 2)])
    return {"n": N, "wells": wells, "pipes": pipes}
