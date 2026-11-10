"""Maximum Depth of Binary Tree with 10^4 nodes: a zigzag chain 10^4 deep, or a random tree."""

from _shapes import level_order

SEEDS = 2
N = 10**4


def generate(rng):
    left, right = [None] * N, [None] * N
    if rng.random() < 0.5:
        for i in range(1, N):
            if rng.random() < 0.5:
                left[i - 1] = i
            else:
                right[i - 1] = i
    else:
        slots = [(0, 0), (0, 1)]
        for i in range(1, N):
            j = rng.randrange(len(slots))
            slots[j], slots[-1] = slots[-1], slots[j]
            parent, side = slots.pop()
            if side == 0:
                left[parent] = i
            else:
                right[parent] = i
            slots.append((i, 0))
            slots.append((i, 1))
    val = [rng.randint(-100, 100) for _ in range(N)]
    return {"root": level_order(val, left, right)}
