"""Add Two Numbers at 100 digits (least significant first): all nines carry every step;
random digits otherwise. The last node is never 0."""

SEEDS = 2


def generate(rng):
    if rng.random() < 0.5:
        return {"l1": [9] * 100, "l2": [1]}
    l1 = [rng.randint(0, 9) for _ in range(99)] + [rng.randint(1, 9)]
    l2 = [rng.randint(0, 9) for _ in range(rng.randint(0, 99))] + [rng.randint(1, 9)]
    return {"l1": l1, "l2": l2}
