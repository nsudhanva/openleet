"""Make String a Subsequence Using Cyclic Increments at |str1| = 2 * 10^4, |str2| = 10^4: str2 is a
spread-out subsequence of str1 with letters shifted by 0 or 1 (half the time the last letter
shifted by 2, so it likely fails), so the O(|str1| |str2|) subsequence DP is 2 * 10^8 steps."""

from string import ascii_lowercase

SEEDS = 2
N = 2 * 10**4
M = 10**4


def _shift(c, d):
    return chr((ord(c) - 97 + d) % 26 + 97)


def generate(rng):
    str1 = "".join(rng.choice(ascii_lowercase) for _ in range(N))
    picks = sorted(rng.sample(range(N), M))
    str2 = [_shift(str1[i], rng.randrange(2)) for i in picks]
    if rng.random() < 0.5:
        # Shift the last letter by 2 so it can only match a later str1 letter, which the
        # spread-out picks make unlikely; the reference decides either way.
        str2[-1] = _shift(str1[picks[-1]], 2)
    return {"str1": str1, "str2": "".join(str2)}
