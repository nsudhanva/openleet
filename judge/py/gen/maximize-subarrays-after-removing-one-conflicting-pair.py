"""Maximize Subarrays After Removing One Conflicting Pair at n = 5000: every right end r has its own
pair [r - d, r] with d <= 3 and the rest of the 2n pairs are random, so every pair binds somewhere
and recounting the valid subarrays per removed pair is ~5 * 10^7 steps."""

SEEDS = 2
N = 5000


def generate(rng):
    pairs = [[max(1, r - rng.randint(1, 3)), r] for r in range(2, N + 1)]
    while len(pairs) < 2 * N:
        pairs.append(rng.sample(range(1, N + 1), 2))
    for pair in pairs:
        if rng.random() < 0.5:
            pair.reverse()
    rng.shuffle(pairs)
    return {"n": N, "conflictingPairs": pairs}
