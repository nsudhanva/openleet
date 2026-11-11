"""Longest Duplicate Substring at n = 25000 random letters with one planted 2000-letter repeat, so
comparing the string with every shift of itself, or trying every length up to the answer,
costs ~6 * 10^8 steps."""

SEEDS = 2
N = 25000
PLANT = 2000


def generate(rng):
    s = [rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(N)]
    a = rng.randrange(0, N // 2 - PLANT)
    b = rng.randrange(N // 2, N - PLANT)
    s[b : b + PLANT] = s[a : a + PLANT]
    return {"s": "".join(s)}
