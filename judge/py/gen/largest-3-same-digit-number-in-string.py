"""Largest 3-Same-Digit Number on 1000-digit strings: random digits, or no three in a row
except one good triple near the end."""

SEEDS = 2
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        return {"num": "".join(rng.choice("0123456789") for _ in range(N))}
    digits = []
    for _ in range(N - 3):
        d = rng.choice("0123456789")
        while len(digits) >= 2 and digits[-1] == digits[-2] == d:
            d = rng.choice("0123456789")
        digits.append(d)
    pos = rng.randint(N - 200, N - 3)
    triple = rng.choice("0123456789") * 3
    return {"num": "".join(digits[:pos]) + triple + "".join(digits[pos:])}
