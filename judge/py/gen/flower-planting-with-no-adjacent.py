"""10^4 gardens joined by ~1.5 * 10^4 random paths, nearly every garden at the limit of 3, so
scanning the whole path list for each garden's neighbours costs ~1.5 * 10^8 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    # Pair up three stubs per garden at random, dropping self-loops and repeated pairs.
    stubs = [v for v in range(1, N + 1) for _ in range(3)]
    rng.shuffle(stubs)
    seen, paths = set(), []
    for i in range(0, len(stubs) - 1, 2):
        x, y = stubs[i], stubs[i + 1]
        if x != y and (min(x, y), max(x, y)) not in seen:
            seen.add((min(x, y), max(x, y)))
            paths.append([x, y])
    return {"n": N, "paths": paths}
