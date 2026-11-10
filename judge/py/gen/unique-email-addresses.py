"""Unique Email Addresses at 100 long addresses whose local names differ only by dots and
'+' suffixes, so normalisation must be exact."""

from _shapes import random_string

SEEDS = 2
N = 100
LETTERS = "abc"


def generate(rng):
    bases = [random_string(rng, LETTERS, rng.randint(1, 8)) for _ in range(15)]
    domains = [random_string(rng, LETTERS + ".", rng.randint(0, 10)) for _ in range(4)]
    domains = [("x" + d) + ".com" for d in domains]
    emails = []
    for _ in range(N):
        base = rng.choice(bases)
        local = ""
        for ch in base:
            local += ch + ("." * rng.randint(0, 2) if rng.random() < 0.3 else "")
        if rng.random() < 0.5:
            local += "+" + random_string(rng, LETTERS + ".+", rng.randint(0, 20))
        email = local + "@" + rng.choice(domains)
        emails.append(email)
    return {"emails": emails}
