"""Check If Strings Can be Made Equal With Operations II at n = 5 * 10^4: each parity class of s1 is
sorted one way and of s2 the other, so fixing positions one swap at a time searches far ahead
every time; one of the three seeds changes the last letter of s2."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    broken = pick_shape(rng) == 2
    s1, s2 = [""] * N, [""] * N
    for parity in (0, 1):
        letters = sorted(rng.choice(ALPHABET) for _ in range(parity, N, 2))
        s1[parity::2] = letters
        s2[parity::2] = letters[::-1]
    if broken:
        s2[-1] = rng.choice([c for c in ALPHABET if c != s2[-1]])
    return {"s1": "".join(s1), "s2": "".join(s2)}
