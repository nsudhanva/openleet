"""Distinct Subsequences with |s| = 1000 and a long t taken as a subsequence of s, for the
full 10^6-cell DP; kept only when the count fits in a signed 32-bit integer."""

SEEDS = 2
L = 1000
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def count(s, t):
    where = {}
    for j, c in enumerate(t):
        where.setdefault(c, []).append(j)
    for c in where:
        where[c].reverse()
    dp = [1] + [0] * len(t)
    for c in s:
        for j in where.get(c, ()):
            dp[j + 1] += dp[j]
    return dp[-1]


def generate(rng):
    while True:
        alphabet = LETTERS if rng.random() < 0.5 else rng.sample(LETTERS, 4)
        s = [rng.choice(alphabet) for _ in range(L)]
        keep = sorted(rng.sample(range(L), rng.randint(L - 40, L - 5)))
        t = "".join(s[i] for i in keep)
        s = "".join(s)
        if count(s, t) <= 2**31 - 1:
            return {"s": s, "t": t}
