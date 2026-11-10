"""Print Binary Tree at the maximum height (depth 10), so the output grid is 10 x 1023: a
random tree, or a full one with all 1023 nodes."""

SEEDS = 2
DEPTH = 10


def generate(rng):
    full = rng.random() < 0.5
    # Heap-indexed positions; keep a spine to guarantee depth exactly 10.
    spine, pos = {1}, 1
    for _ in range(DEPTH - 1):
        pos = 2 * pos + rng.randint(0, 1)
        spine.add(pos)
    present = set(spine)
    for p in range(2, 2**DEPTH):
        if p // 2 in present and (full or rng.random() < 0.6):
            present.add(p)
    # Level-order serialization: BFS over present heap indices.
    out, queue, head = [], [1], 0
    while head < len(queue):
        p = queue[head]
        head += 1
        if p not in present:
            out.append(None)
            continue
        out.append(rng.randint(-99, 99))
        if p < 2 ** (DEPTH - 1):
            queue.extend([2 * p, 2 * p + 1])
        else:
            queue.extend([0, 0])
    while out and out[-1] is None:
        out.pop()
    return {"root": out}
