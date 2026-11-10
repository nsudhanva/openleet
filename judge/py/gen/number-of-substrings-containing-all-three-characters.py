"""All Three Characters at length 5 * 10^4: random abc, or long single-letter runs so a
substring must stretch far to contain all three."""

from _shapes import random_string

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        s = random_string(rng, "abc", N)
    else:
        parts, total = [], 0
        while total < N:
            run = min(rng.randint(1, 5000), N - total)
            parts.append(rng.choice("abc") * run)
            total += run
        s = "".join(parts)
        s = "abc" + s[3:]
    return {"s": s}
