"""Minimize Hamming Distance After Swap Operations at n = 3 * 10^4 with 3 * 10^4 random swaps,
so merging groups by relabelling every index costs ~10^9 steps."""

SEEDS = 2
N = 3 * 10**4
E = 3 * 10**4


def generate(rng):
    source = [rng.randint(1, 100) for _ in range(N)]
    target = [x if rng.random() < 0.5 else rng.randint(1, 100) for x in source]
    rng.shuffle(target)
    swaps = []
    for _ in range(E):
        a, b = rng.sample(range(N), 2)
        swaps.append([a, b])
    return {"source": source, "target": target, "allowedSwaps": swaps}
