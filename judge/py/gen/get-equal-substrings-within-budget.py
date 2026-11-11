"""s and t of 3 * 10^4 letters differing by ~4 per position, with a budget of about half the
total cost, so extending a window from every start costs ~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    s = [rng.randrange(26) for _ in range(N)]
    t = [min(25, max(0, c + rng.randint(-8, 8))) for c in s]
    cost = sum(abs(a - b) for a, b in zip(s, t, strict=True))
    return {
        "s": "".join(ALPHABET[c] for c in s),
        "t": "".join(ALPHABET[c] for c in t),
        "maxCost": min(10**6, cost // 2 + rng.randint(0, 100)),
    }
