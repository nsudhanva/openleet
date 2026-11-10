"""Populating Next Right Pointers II on a 6000-node tree: a random shape with ragged levels,
or a deep sparse one where next pointers must skip long gaps."""

SEEDS = 2
N = 6000


def build(rng, n, deep):
    left, right = [-1] * n, [-1] * n
    slots = [(0, 0), (0, 1)]
    for v in range(1, n):
        if deep:
            i = len(slots) - 1 - min(len(slots) - 1, int(rng.expovariate(0.5)))
        else:
            i = rng.randrange(len(slots))
        slots[i], slots[-1] = slots[-1], slots[i]
        parent, side = slots.pop()
        (left if side == 0 else right)[parent] = v
        slots.append((v, 0))
        slots.append((v, 1))
    return left, right


def generate(rng):
    left, right = build(rng, N, rng.random() < 0.5)
    vals = [rng.randint(-100, 100) for _ in range(N)]
    out, queue, head = [], [0], 0
    while head < len(queue):
        v = queue[head]
        head += 1
        if v == -1:
            out.append(None)
            continue
        out.append(vals[v])
        queue.append(left[v])
        queue.append(right[v])
    while out and out[-1] is None:
        out.pop()
    return {"root": out}
