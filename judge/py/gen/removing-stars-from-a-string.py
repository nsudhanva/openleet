"""Removing Stars From a String at n = 10^5 with every star after every letter, so deleting one
star and its letter at a time rebuilds a ~10^5-character string 5 * 10^4 times."""

SEEDS = 2
N = 10**5


def generate(rng):
    letters = N // 2 + rng.randrange(100)
    head = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(letters))
    return {"s": head + "*" * (N - letters)}
