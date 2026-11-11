"""The lcp matrix of 'a' * 500 or of a period-2 string of 600, about 1 MB, so its entries
average ~170 (or ~100) and checking each one by comparing the suffixes costs ~4 * 10^7
character steps."""

SEEDS = 2


def generate(rng):
    period = 1 + rng.getrandbits(1)
    n = 500 if period == 1 else 600
    letters = rng.sample("abcdefghijklmnopqrstuvwxyz", period)
    s = "".join(letters[i % period] for i in range(n))
    # lcp[i][j] = lcp[i + 1][j + 1] + 1 where s[i] == s[j], built one row at a time.
    lcp, nxt = [None] * n, [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        c = s[i]
        row = [nxt[j + 1] + 1 if s[j] == c else 0 for j in range(n)]
        lcp[i] = row
        nxt = [*row, 0]
    return {"lcp": lcp}
