"""Valid K-Palindrome at 300 random letters with k one short of enough (false), so the DP fills
every cell and trying both deletions at each mismatch without memoizing is exponential."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 300


def generate(rng):
    s = random_string(rng, ascii_lowercase, N)
    # Longest palindromic subsequence; deleting n - lps characters is the minimum.
    prev = [0] * (N + 1)
    for i in range(N - 1, -1, -1):
        cur = [0] * (N + 1)
        cur[i] = 1
        for j in range(i + 1, N):
            cur[j] = prev[j - 1] + 2 if s[i] == s[j] else max(prev[j], cur[j - 1])
        prev = cur
    return {"s": s, "k": N - prev[N - 1] - 1}
