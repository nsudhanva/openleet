"""Palindromic Permutation Greater Than Target at n near 300: s always has a palindromic
arrangement over a small alphabet, and target sits near (just below, at, or randomly around)
one of those palindromes."""

from string import ascii_lowercase

SEEDS = 3


def generate(rng):
    n = rng.choice([300, 299])
    alphabet = ascii_lowercase[: rng.randint(2, 6)]
    half = [rng.choice(alphabet) for _ in range(n // 2)]
    middle = [rng.choice(alphabet)] if n % 2 else []
    pal = half + middle + half[::-1]
    s = pal[:]
    rng.shuffle(s)
    shape = rng.choice(["equal", "below", "random"])
    if shape == "random":
        target = [rng.choice(alphabet) for _ in range(n)]
    else:
        target = sorted(half) + middle + sorted(half)[::-1]
        if shape == "below":
            pos = rng.randrange(n)
            if target[pos] != "a":
                target[pos] = chr(ord(target[pos]) - 1)
    return {"s": "".join(s), "target": "".join(target)}
