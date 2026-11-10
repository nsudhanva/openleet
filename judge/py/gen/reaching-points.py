"""Reaching Points with targets near 10^9 built by long runs of the same move from a small
start (reachable), or the same target nudged by one; forward search explodes."""

SEEDS = 3


def generate(rng):
    sx, sy = rng.randint(1, 10), rng.randint(1, 10)
    x, y = sx, sy
    while True:
        if rng.random() < 0.5:
            k = rng.randint(1, max(1, (10**9 - x) // y // 2))
            if x + k * y > 10**9:
                break
            x += k * y
        else:
            k = rng.randint(1, max(1, (10**9 - y) // x // 2))
            if y + k * x > 10**9:
                break
            y += k * x
        if max(x, y) > 10**8 and rng.random() < 0.3:
            break
    if rng.random() < 0.3:
        x = x - 1 if x > 1 else x + 1
    return {"sx": sx, "sy": sy, "tx": x, "ty": y}
