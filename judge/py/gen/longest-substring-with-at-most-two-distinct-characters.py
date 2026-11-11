"""Longest Substring with At Most Two Distinct Characters at 3 * 10^4 letters: two letters with a
third appearing only 3 times, so windows span ~n / 4 and growing one from every start is
~10^8 steps."""

from string import ascii_letters

SEEDS = 2
N = 3 * 10**4
RARE = 3


def generate(rng):
    a, b, rare = rng.sample(ascii_letters, 3)
    s = [rng.choice((a, b)) for _ in range(N)]
    for i in rng.sample(range(N), RARE):
        s[i] = rare
    return {"s": "".join(s)}
