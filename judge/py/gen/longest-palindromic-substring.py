"""Longest Palindromic Substring at length 1000 with a unique answer: one letter repeated
(cubic checks time out), or random text with one long palindrome planted inside."""

from string import ascii_letters, digits

SEEDS = 2
N = 1000
CHARS = ascii_letters + digits


def generate(rng):
    if rng.random() < 0.5:
        return {"s": rng.choice(CHARS) * N}
    length = rng.randint(300, 600)
    half = [rng.choice(CHARS) for _ in range(length // 2)]
    middle = [rng.choice(CHARS)] if length % 2 else []
    pal = half + middle + half[::-1]
    rest = N - length
    left = rng.randint(0, rest)
    noise = [rng.choice(CHARS) for _ in range(rest)]
    return {"s": "".join(noise[:left] + pal + noise[left:])}
