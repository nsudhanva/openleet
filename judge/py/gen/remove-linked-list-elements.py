"""Remove Linked List Elements at 10^4 nodes: mostly the target value (including the head
run), or a random mix."""

SEEDS = 2


def generate(rng):
    val = rng.randint(1, 50)
    p = rng.choice([0.9, 0.1])
    head = [val if rng.random() < p else rng.randint(1, 50) for _ in range(10**4)]
    return {"head": head, "val": val}
