"""Sum of Scores of Built Strings at n = 5 * 10^4: one letter repeated or a short block repeated, so
matching each suffix against the whole string character by character is ~10^9 steps."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    block = "".join(rng.choice("ab") for _ in range(rng.choice((1, 3, 7))))
    s = (block * (N // len(block) + 1))[:N]
    i = rng.randrange(N - 50, N)
    return {"s": s[:i] + rng.choice("xyz") + s[i + 1 :]}
