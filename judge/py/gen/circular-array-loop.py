"""Circular Array Loop at n = 5000 (or 1000): one all-forward cycle through every index (true),
all self-loops (false), blocks that bounce back and forth or direction-flipping neighbours
(false, every start fails), or random jumps."""

SEEDS = 3


def generate(rng):
    shape = rng.choice(["one-cycle", "self", "bounce", "flip", "random"])
    n = 5000
    if shape == "one-cycle":
        nums = [1] * n
    elif shape == "self":
        n = 1000
        nums = [rng.choice([1000, -1000]) for _ in range(n)]
    elif shape == "bounce":
        nums = [1000 if (i // 1000) % 2 == 0 else -1000 for i in range(n)]
    elif shape == "flip":
        nums = [1 if i % 2 == 0 else -1 for i in range(n)]
    else:
        nums = [rng.choice([1, -1]) * rng.randint(1, 1000) for _ in range(n)]
    return {"nums": nums}
