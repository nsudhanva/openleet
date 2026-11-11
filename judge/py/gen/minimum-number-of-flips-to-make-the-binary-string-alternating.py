"""Minimum Number of Flips to Make the Binary String Alternating at odd n = 99,999: an
alternating string with one rotation seam and noise, so counting mismatches for every rotation
is ~10^10 steps, and even re-parsing every rotated string as a binary number is ~10^10 digits."""

SEEDS = 2
N = 99999


def generate(rng):
    # An odd-length alternating string rotated at a random point has a "00" or "11" seam that
    # only the right rotation removes; the noise keeps the best count above zero.
    s = [str(i & 1) for i in range(N)]
    cut = rng.randrange(N)
    s = s[cut:] + s[:cut]
    for i in rng.sample(range(N), max(1, N // 50)):
        s[i] = "1" if s[i] == "0" else "0"
    return {"s": "".join(s)}
