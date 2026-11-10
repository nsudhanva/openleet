"""Minimum Window Substring at |s| = 10^5: t of a few hundred letters with the matching
window near the end, or t as long as s, so re-checking each window is quadratic."""

from string import ascii_letters

from _shapes import random_string

SEEDS = 3
N = 10**5


def generate(rng):
    kind = rng.choice(("short", "long", "small-alphabet"))
    if kind == "small-alphabet":
        s = random_string(rng, "ab", N)
        t = random_string(rng, "ab", rng.randint(1, 1000))
        return {"s": s, "t": t}
    s = [rng.choice(ascii_letters[:26]) for _ in range(N)]
    if kind == "short":
        t = [rng.choice(ascii_letters) for _ in range(300)]
        pos = rng.randint(N - 1000, N - 600)
        for i, ch in enumerate(t):
            s[pos + 2 * i] = ch
    else:
        t = s[:]
        rng.shuffle(t)
        t[rng.randrange(N)] = rng.choice(ascii_letters)
    return {"s": "".join(s), "t": "".join(t)}
