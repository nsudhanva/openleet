"""Interleaving String at the maximum lengths (100 + 100 = 200), false although s3 holds exactly the
letters of s1 and s2, with the mismatch near s3's middle or end, so recursion without memoization
tries exponentially many splits before it fails."""

from string import ascii_lowercase

SEEDS = 2
N = 100


def interleaves(s1, s2, s3):
    row = [True] + [False] * len(s2)
    for j in range(1, len(s2) + 1):
        row[j] = row[j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, len(s1) + 1):
        row[0] = row[0] and s1[i - 1] == s3[i - 1]
        for j in range(1, len(s2) + 1):
            c = s3[i + j - 1]
            row[j] = (row[j] and s1[i - 1] == c) or (row[j - 1] and s2[j - 1] == c)
    return row[-1]


def generate(rng):
    a, b = rng.sample(ascii_lowercase, 2)
    if rng.random() < 0.5:
        # s3 needs s2's lone b before s2 has had time to reach it: every split dies there.
        s1, s2 = a * N, a * (N - 1) + b
        p = rng.randint(N - 8, N - 2)
        s3 = a * p + b + a * (2 * N - 1 - p)
        if rng.random() < 0.5:
            s1, s2 = s2, s1
        return {"s1": s1, "s2": s2, "s3": s3}
    # Both strings are the same pattern and s3 doubles each letter, then the latest pair of
    # letters whose swap (keeping the letter counts) leaves no valid split trade places.
    s1 = s2 = "".join(rng.choice((a, b)) for _ in range(N))
    out = [c for ch in s1 for c in (ch, ch)]
    for k in range(2 * N - 2, -1, -1):
        for k2 in range(k + 1, 2 * N):
            if out[k] != out[k2]:
                s3 = out[:]
                s3[k], s3[k2] = s3[k2], s3[k]
                if not interleaves(s1, s2, s3):
                    return {"s1": s1, "s2": s2, "s3": "".join(s3)}
    raise AssertionError("no false swap")
