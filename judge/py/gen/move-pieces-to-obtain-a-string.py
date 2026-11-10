"""Move Pieces to Obtain a String at n = 10^5: a reachable target built by sliding each L
left and each R right without crossing, or that target with one piece flipped (unreachable)."""

SEEDS = 3
N = 10**5


def generate(rng):
    count = rng.randint(N // 10, N // 2)
    slots = sorted(rng.sample(range(N), count))
    pieces = [rng.choice("LR") for _ in range(count)]
    start = ["_"] * N
    for p, ch in zip(slots, pieces, strict=True):
        start[p] = ch
    # Keep t[i-1] < t[i] < slots[i + 1]: every later piece then still has room.
    target = ["_"] * N
    prev = -1
    for i, (p, ch) in enumerate(zip(slots, pieces, strict=True)):
        nxt = slots[i + 1] if i + 1 < count else N
        q = (
            rng.randint(max(prev + 1, p - 50), p)
            if ch == "L"
            else rng.randint(p, min(nxt - 1, p + 50))
        )
        target[q] = ch
        prev = q
    if rng.random() < 0.5:
        q = rng.choice([i for i, ch in enumerate(target) if ch != "_"])
        target[q] = "L" if target[q] == "R" else "R"
    return {"start": "".join(start), "target": "".join(target)}
