"""Reverse Nodes in Even Length Groups at the maximum length, 10^5 nodes (or one short of a
group boundary, so the last group is partial)."""

SEEDS = 2


def generate(rng):
    n = 10**5 if rng.random() < 0.5 else 446 * 447 // 2 - 1
    return {"head": [rng.randint(0, 10**5) for _ in range(n)]}
