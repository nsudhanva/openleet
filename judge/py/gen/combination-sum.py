"""Combination Sum at target up to 40 with up to 30 distinct candidates, the target chosen as
large as possible while the number of combinations stays under the guaranteed 150."""

SEEDS = 3


def generate(rng):
    size = rng.choice([30, 15, 6])
    lo = rng.choice([2, 5, 8])
    candidates = rng.sample(range(lo, 41), min(size, 41 - lo))
    count = [0] * 41
    count[0] = 1
    for c in candidates:
        for t in range(c, 41):
            count[t] += count[t - c]
    ok = [t for t in range(1, 41) if count[t] < 150]
    best = [t for t in ok if count[t] > 0][-5:] or ok[-1:]
    return {"candidates": candidates, "target": rng.choice(best)}
