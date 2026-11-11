"""Longest Substring with At Most K Distinct Characters at 3 * 10^4 letters: k + 1 letters where
the extra one appears only 3 times, so windows span ~n / 4 and growing one from every start
is ~10^8 steps."""

from string import ascii_lowercase

SEEDS = 2
N = 3 * 10**4
RARE = 3


def generate(rng):
    k = rng.randint(5, 25)
    letters = rng.sample(ascii_lowercase, k + 1)
    common, rare = letters[:k], letters[k]
    s = [rng.choice(common) for _ in range(N)]
    for i in rng.sample(range(N), RARE):
        s[i] = rare
    return {"s": "".join(s), "k": k}
