"""Subsequence After One Replacement at |t| = 2 * 10^4 and |s| = |t| - 20 cut from t over
'ab', with one or two letters flipped near the end, so trying each replacement index with a
fresh subsequence scan is ~4 * 10^8 steps."""

from _shapes import random_string

SEEDS = 2
N = 2 * 10**4
SLACK = 20


def generate(rng):
    # The first draw picks the answer (one flip: true, two: false), so seeds 0 and 1 differ.
    flips = 1 if rng.random() < 0.5 else 2
    t = random_string(rng, "ab", N)
    keep = sorted(rng.sample(range(N), N - SLACK))
    s = [t[i] for i in keep]
    for p in rng.sample(range(len(s) - 200, len(s)), flips):
        s[p] = "c"
    return {"s": "".join(s), "t": t}
