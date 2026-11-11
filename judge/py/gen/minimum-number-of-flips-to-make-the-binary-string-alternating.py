"""Minimum Number of Flips to Make the Binary String Alternating at odd n = 20,001: an
alternating string with one rotation seam and noise, so counting mismatches for every rotation
is ~4 * 10^8 steps."""

SEEDS = 2
N = 20001


def generate(rng):
    # An odd-length alternating string rotated at a random point has a "00" or "11" seam that
    # only the right rotation removes; the noise keeps the best count above zero.
    s = [str(i & 1) for i in range(N)]
    cut = rng.randrange(N)
    s = s[cut:] + s[:cut]
    for i in rng.sample(range(N), max(1, N // 50)):
        s[i] = "1" if s[i] == "0" else "0"
    return {"s": "".join(s)}
