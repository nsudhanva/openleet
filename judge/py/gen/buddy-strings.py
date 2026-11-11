"""Buddy Strings at length 10^4: strings that differ only in the last two positions (a valid
swap) or by rotating three distinct letters near the end (same letter counts, no swap), so
trying every pair of positions scans ~5 * 10^7 pairs before deciding."""

from string import ascii_lowercase

SEEDS = 2
N = 10**4


def generate(rng):
    s = [rng.choice(ascii_lowercase) for _ in range(N)]
    a, b, c = rng.sample(ascii_lowercase, 3)
    if rng.random() < 0.5:
        s[-2], s[-1] = a, b
        goal = list(s)
        goal[-2], goal[-1] = b, a
    else:
        i, j, k = sorted(rng.sample(range(N - 10, N), 3))
        s[i], s[j], s[k] = a, b, c
        goal = list(s)
        goal[i], goal[j], goal[k] = b, c, a
    return {"s": "".join(s), "goal": "".join(goal)}
