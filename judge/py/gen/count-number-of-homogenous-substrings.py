"""Count Number of Homogenous Substrings at length 6 * 10^4 made of a few runs thousands of
characters long, so extending every start along its run costs ~4 * 10^8 steps."""

SEEDS = 2
N = 6 * 10**4
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    parts, total, last = [], 0, ""
    while total < N:
        run = min(N - total, rng.randint(N // 8, N // 3))
        c = rng.choice([a for a in ALPHABET if a != last])
        parts.append(c * run)
        total += run
        last = c
    return {"s": "".join(parts)}
