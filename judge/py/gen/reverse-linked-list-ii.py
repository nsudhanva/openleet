"""Reverse Linked List II at n = 500 with a wide or full [left, right] window."""

SEEDS = 3


def generate(rng):
    n = 500
    head = [rng.randint(-500, 500) for _ in range(n)]
    if rng.random() < 0.5:
        left, right = 1, n
    else:
        left = rng.randint(1, n)
        right = rng.randint(left, n)
    return {"head": head, "left": left, "right": right}
