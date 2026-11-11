"""Number of Substrings With Only 1s at 5 * 10^4 characters in runs of 1s 6,000 to 20,000 long, so
extending a substring from every position costs ~4 * 10^8 steps."""

SEEDS = 2
N = 5 * 10**4
LONG = 2 * 10**4


def generate(rng):
    s = ""
    while len(s) < N:
        s += "1" * rng.randint(LONG * 3 // 10, LONG) + "0" * rng.randint(1, 3)
    return {"s": s[:N]}
