"""Build a tree from inorder and preorder traversals at 3000 distinct values: a chain 3000
deep (recursion and linear-index-search worst case), a deep mostly-chain tree, or a random tree."""

SEEDS = 3
N = 3000


def _shape(rng, n, kind):
    """Child index lists for an n-node tree rooted at 0: 'random', 'chain' or 'deep'."""
    left, right = [None] * n, [None] * n
    slots = [(0, 0), (0, 1)]
    for i in range(1, n):
        if kind == "chain" or (kind == "deep" and rng.random() < 0.9):
            parent, side = i - 1, rng.randrange(2)
            if (left, right)[side][parent] is not None:
                side = 1 - side
        else:
            while True:
                j = rng.randrange(len(slots))
                slots[j], slots[-1] = slots[-1], slots[j]
                parent, side = slots.pop()
                if (left, right)[side][parent] is None:
                    break
        (left, right)[side][parent] = i
        slots.append((i, 0))
        slots.append((i, 1))
    return left, right


def _orders(left, right):
    pre, ino, post = [], [], []
    stack = [(0, 0)]
    while stack:
        node, state = stack.pop()
        if state == 0:
            pre.append(node)
            stack.append((node, 1))
            if left[node] is not None:
                stack.append((left[node], 0))
        elif state == 1:
            ino.append(node)
            stack.append((node, 2))
            if right[node] is not None:
                stack.append((right[node], 0))
        else:
            post.append(node)
    return pre, ino, post


def generate(rng):
    left, right = _shape(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = rng.sample(range(-3000, 3001), N)
    pre, ino, _ = _orders(left, right)
    return {"preorder": [vals[i] for i in pre], "inorder": [vals[i] for i in ino]}
