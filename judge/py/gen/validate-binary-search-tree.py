"""Validate BST at 10^4 nodes spanning the full 32-bit range (including -2^31 and 2^31 - 1):
a valid BST, or one deep leaf that obeys its parent but breaks an ancestor's bound or
equals it."""

SEEDS = 3
N = 10**4
LO, HI = -(2**31), 2**31 - 1


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    values = [*rng.sample(range(LO + 1, HI), N - 2), LO, HI]
    rng.shuffle(values)
    left, right = {}, {}
    root = values[0]
    for v in values[1:]:
        cur = root
        while True:
            side = left if v < cur else right
            if cur in side:
                cur = side[cur]
            else:
                side[cur] = v
                break
    rename = {}
    if shape > 0:
        # The deepest leaf whose far-side bound comes from an ancestor (not its parent).
        best = None
        stack = [(root, None, None, 0, None)]
        while stack:
            node, lo, hi, depth, parent = stack.pop()
            if node not in left and node not in right and parent is not None:
                far = lo if left.get(parent) == node else hi
                if far is not None and (best is None or depth > best[0]):
                    best = (depth, node, parent, far)
            if node in left:
                stack.append((left[node], lo, node, depth + 1, node))
            if node in right:
                stack.append((right[node], node, hi, depth + 1, node))
        _, leaf, parent, far = best
        # Equal to the ancestor (invalid under strict ordering), or just past its bound.
        past = far - 1 if far < parent else far + 1
        rename[leaf] = far if shape == 1 or far in (LO, HI) else past
    out, queue, i = [], [root], 0
    while i < len(queue):
        node = queue[i]
        i += 1
        if node is None:
            out.append(None)
            continue
        out.append(rename.get(node, node))
        queue.append(left.get(node))
        queue.append(right.get(node))
    while out and out[-1] is None:
        out.pop()
    return {"root": out}
