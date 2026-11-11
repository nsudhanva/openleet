"""Merge Nodes in Between Zeros at 4 * 10^4 nodes in runs of one or two values, so appending each
merged node by walking from the head costs ~2 * 10^8 steps."""

SEEDS = 2
N = 4 * 10**4


def generate(rng):
    head = [0]
    while len(head) < N - 2:
        head += [rng.randint(1, 1000) for _ in range(rng.randint(1, 2))]
        head.append(0)
    return {"head": head}
