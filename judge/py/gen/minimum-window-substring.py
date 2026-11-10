"""Minimum Window Substring at |s| = 10^5: t of a few hundred letters with the matching
window near the end, or t as long as s, so re-checking each window is quadratic."""

SEEDS = 3
N = 10**5
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate(rng):
    kind = rng.choice(("short", "long", "small-alphabet"))
    if kind == "small-alphabet":
        s = "".join(rng.choice("ab") for _ in range(N))
        t = "".join(rng.choice("ab") for _ in range(rng.randint(1, 1000)))
        return {"s": s, "t": t}
    s = [rng.choice(LETTERS[:26]) for _ in range(N)]
    if kind == "short":
        t = [rng.choice(LETTERS) for _ in range(300)]
        pos = rng.randint(N - 1000, N - 600)
        for i, ch in enumerate(t):
            s[pos + 2 * i] = ch
    else:
        t = s[:]
        rng.shuffle(t)
        t[rng.randrange(N)] = rng.choice(LETTERS)
    return {"s": "".join(s), "t": "".join(t)}
