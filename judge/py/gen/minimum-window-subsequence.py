"""Minimum Window Subsequence at |s1| = 2 * 10^4 over 'ab' whose only 'z' is last, with s2 a short
'a'/'b' prefix then 'z', so matching s2 forward from every start scans to the end: ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4
K = 5


def generate(rng):
    s1 = "".join(rng.choice("ab") for _ in range(N - 1)) + "z"
    s2 = "".join(rng.choice("ab") for _ in range(K - 1)) + "z"
    return {"s1": s1, "s2": s2}
