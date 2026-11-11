"""Minimum Number of Steps to Make Two Strings Anagram at length 5 * 10^4 with s sorted and t
sorted the other way, so matching each letter of t by searching a list of s and removing it
scans past ~n / 2 letters each time."""

SEEDS = 2
N = 5 * 10**4
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    s = sorted(rng.choice(ALPHABET) for _ in range(N))
    t = sorted((rng.choice(ALPHABET) for _ in range(N)), reverse=True)
    return {"s": "".join(s), "t": "".join(t)}
