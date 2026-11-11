"""s of 10^5 letters and a pattern of about half that length differing from every window in two
letters, late in the pattern on one seed and in its middle on the others, with the first
one-mismatch window near the end, so checking windows from either end costs over 10^9."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    m = rng.randint(N // 2 - 1000, N // 2 + 1000)
    c, d = rng.sample("abcdefghijklmnopqrstuvwxyz", 2)
    # The pattern is c * m with d at a < b; s is c * N with one d at q. A window at i is one change
    # away only when q - i is a or b, so the answer is q - b, near the end. Late a and b defeat a
    # binary search for the first mismatch; middle ones defeat a scan from both ends.
    if shape == 0:
        b = m - 1
        a = b - rng.randint(1, 50)
    else:
        a = m // 2 - rng.randint(1, 50)
        b = a + rng.randint(1, 50)
    pattern = [c] * m
    pattern[a] = pattern[b] = d
    q = N - m + b - rng.randint(1, 50)
    s = [c] * N
    s[q] = d
    return {"s": "".join(s), "pattern": "".join(pattern)}
