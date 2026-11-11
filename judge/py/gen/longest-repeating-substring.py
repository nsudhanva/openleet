"""Longest Repeating Substring at n = 1500 with a tiny period and a few changed letters, so
measuring the common prefix of every pair of positions costs ~5 * 10^8 steps."""

SEEDS = 2
N = 1500


def generate(rng):
    period = "".join(rng.choice("abc") for _ in range(rng.randint(1, 2)))
    s = list((period * N)[:N])
    for _ in range(rng.randint(2, 5)):
        s[rng.randrange(N)] = rng.choice("abcdefghijklmnopqrstuvwxyz")
    return {"s": "".join(s)}
