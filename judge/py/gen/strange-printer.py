"""Strange Printer at length 100 (O(n^3) interval DP): random over a few letters, or an
alternating pattern that defeats greedy merges."""

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        s = "".join(rng.choice("abc") for _ in range(100))
    elif shape == 1:
        s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(100))
    else:
        s = ("ab" * 50) if rng.random() < 0.5 else ("abcba" * 20)
    return {"s": s}
