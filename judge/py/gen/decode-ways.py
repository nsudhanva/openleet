"""Decode Ways at length 100 built mostly from 1s and 2s, where naive recursion explodes;
each digit is chosen so the count stays within a 32-bit integer as the statement guarantees."""

SEEDS = 2
L = 100
LIMIT = 2**31 - 1


def step(s, prev, cur, ch):
    nxt = cur if ch != "0" else 0
    if s and (s[-1] == "1" or (s[-1] == "2" and ch <= "6")):
        nxt += prev
    return cur, nxt


def generate(rng):
    s, prev, cur = "", 1, 1
    bias = rng.choice([0.75, 0.9])
    for _ in range(L):
        first = rng.choice("12") if rng.random() < bias else rng.choice("0123456789")
        # Fallback: '0' after a 1 or 2 keeps the previous count; '7' elsewhere keeps the current.
        safe = "0" if s and s[-1] in "12" else "7"
        for ch in (first, safe):
            p, c = step(s, prev, cur, ch)
            if 0 < c <= LIMIT:
                break
        s, prev, cur = s + ch, p, c
    return {"s": s}
