"""Count Number of Texts at 2 * 10^4 key presses in runs hundreds to thousands long, so
splitting a run by trying every message without memoizing takes exponential time."""

SEEDS = 2
N = 2 * 10**4
KEYS = "23456789"


def generate(rng):
    parts, total = [], 0
    while total < N:
        run = min(N - total, rng.randint(1, 2000))
        parts.append(rng.choice(KEYS) * run)
        total += run
    return {"pressedKeys": "".join(parts)}
