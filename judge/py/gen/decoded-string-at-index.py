"""Decoded String at Index with |s| = 100 whose decoded length is astronomically large (kept
below 2^63), so expanding the string is impossible; k up to 10^9."""

SEEDS = 2
L = 100
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    s = [rng.choice(LETTERS)]
    size = 1
    digit_p = rng.choice([0.3, 0.6])
    while len(s) < L:
        if rng.random() < digit_p:
            d = rng.randint(2, 9)
            if size * d < 2**63:
                s.append(str(d))
                size *= d
                continue
        s.append(rng.choice(LETTERS))
        size += 1
    if size >= 2**63:
        raise ValueError("decoded length too large")
    top = min(size, 10**9)
    k = top if rng.random() < 0.3 else rng.randint(max(1, top // 2), top)
    return {"s": "".join(s), "k": k}
