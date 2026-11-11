"""Building blocks shared by the stress-test generators in this directory.

A binary tree is a pair of child lists: left[i] and right[i] hold node i's children or the
`empty` marker (None by default, -1 where a generator keeps the lists all-int). Node 0 is the
root unless a builder returns one. Stored stress tests are keyed by the hash of each seed's
input, so every function here must keep drawing from rng in exactly the same order.
"""

from collections import deque
from collections.abc import Iterable, Sequence
from random import Random

type Children = tuple[list, list]


def pick_shape(rng: Random) -> int:
    """0, 1 or 2, drawn so that seeds 0, 1 and 2 each land on a different one."""
    return rng.getrandbits(6) % 3


def random_string(rng: Random, alphabet: Sequence[str], length: int) -> str:
    """length characters, each drawn independently from alphabet."""
    return "".join(rng.choice(alphabet) for _ in range(length))


def level_order(
    vals: Sequence,
    left: list,
    right: list,
    root: int = 0,
    empty: int | None = None,
) -> list:
    """LeetCode's level-order list for the tree, with trailing Nones dropped."""
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node == empty:
            out.append(None)
        else:
            out.append(vals[node])
            queue.extend((left[node], right[node]))
    while out and out[-1] is None:
        out.pop()
    return out


def inorder(left: list, right: list, root: int = 0, empty: int | None = None) -> list[int]:
    """Node ids in in-order."""
    order, stack, node = [], [], root
    while stack or node != empty:
        while node != empty:
            stack.append(node)
            node = left[node]
        node = stack.pop()
        order.append(node)
        node = right[node]
    return order


def traversals(
    left: list, right: list, root: int = 0, empty: int | None = None
) -> tuple[list[int], list[int], list[int]]:
    """Node ids in pre-order, in-order and post-order."""
    pre, ino, post = [], [], []
    stack = [(root, 0)]
    while stack:
        node, state = stack.pop()
        if state == 0:
            pre.append(node)
            stack.append((node, 1))
            if left[node] != empty:
                stack.append((left[node], 0))
        elif state == 1:
            ino.append(node)
            stack.append((node, 2))
            if right[node] != empty:
                stack.append((right[node], 0))
        else:
            post.append(node)
    return pre, ino, post


def leaf_sums(vals: Sequence[int], left: list, right: list, empty: int | None = None) -> list[int]:
    """Every path sum from the root (node 0) to a leaf."""
    sums, stack = [], [(0, vals[0])]
    while stack:
        node, total = stack.pop()
        if left[node] == empty and right[node] == empty:
            sums.append(total)
        for child in (left[node], right[node]):
            if child != empty:
                stack.append((child, total + vals[child]))
    return sums


def random_tree(rng: Random, n: int, empty: int | None = None, swap: bool = True) -> Children:
    """A random n-node tree: each new node fills an open child slot chosen uniformly. With swap
    False the chosen slot is popped in place rather than swapped to the end first, which leaves
    the open slots in a different order, so the same rng grows a different tree."""
    left, right = [empty] * n, [empty] * n
    slots = [(0, 0), (0, 1)]
    for i in range(1, n):
        j = rng.randrange(len(slots))
        if swap:
            slots[j], slots[-1] = slots[-1], slots[j]
            j = -1
        parent, side = slots.pop(j)
        (left, right)[side][parent] = i
        slots += [(i, 0), (i, 1)]
    return left, right


def thin_tree(rng: Random, n: int, window: int, empty: int | None = None) -> Children:
    """A long, thin n-node tree: each new node fills one of the `window` newest open slots."""
    left, right = [empty] * n, [empty] * n
    slots = [(0, 0), (0, 1)]
    for i in range(1, n):
        parent, side = slots.pop(len(slots) - 1 - rng.randrange(min(window, len(slots))))
        (left, right)[side][parent] = i
        slots += [(i, 0), (i, 1)]
    return left, right


def skewed_tree(rng: Random, n: int, empty: int | None = None, rate: float = 1.0) -> Children:
    """A deep n-node tree: each new node fills the k-th newest open slot, k ~ Exp(rate)."""
    left, right = [empty] * n, [empty] * n
    slots = [(0, 0), (0, 1)]
    for i in range(1, n):
        j = len(slots) - 1 - min(len(slots) - 1, int(rng.expovariate(rate)))
        slots[j], slots[-1] = slots[-1], slots[j]
        parent, side = slots.pop()
        (left, right)[side][parent] = i
        slots += [(i, 0), (i, 1)]
    return left, right


def zigzag_path(rng: Random, n: int, empty: int | None = None) -> Children:
    """The path 0 -> 1 -> ... -> n - 1, each node a left child with probability 1/2."""
    left, right = [empty] * n, [empty] * n
    for i in range(1, n):
        (left if rng.random() < 0.5 else right)[i - 1] = i
    return left, right


def shaped_tree(rng: Random, n: int, kind: str) -> Children:
    """An n-node tree of one kind: 'random', 'chain' (a path, each child on a random side) or
    'deep' (a chain with one node in ten attached at random instead)."""
    left, right = [None] * n, [None] * n
    slots = [(0, 0), (0, 1)]
    for i in range(1, n):
        if kind == "chain" or (kind == "deep" and rng.random() < 0.9):
            parent, side = i - 1, rng.randrange(2)
        else:
            while True:
                j = rng.randrange(len(slots))
                slots[j], slots[-1] = slots[-1], slots[j]
                parent, side = slots.pop()
                if (left, right)[side][parent] is None:
                    break
        (left, right)[side][parent] = i
        slots += [(i, 0), (i, 1)]
    return left, right


def insert_bst(vals: Sequence, order: Iterable[int], empty: int | None = None) -> Children:
    """Children of the BST made by inserting the nodes of `order` (the first is the root),
    keyed by vals with equal keys going right. It is built as a Cartesian tree (in-order by
    key, heap-ordered by insertion time), so a sorted order, which makes a chain, costs
    O(n log n) rather than O(n^2)."""
    time = {node: t for t, node in enumerate(order)}
    left, right = [empty] * len(vals), [empty] * len(vals)
    stack = []
    for node in sorted(order, key=lambda i: (vals[i], time[i])):
        last = empty
        while stack and time[stack[-1]] > time[node]:
            last = stack.pop()
        left[node] = last
        if stack:
            right[stack[-1]] = node
        stack.append(node)
    return left, right


def random_bst(rng: Random, n: int, lean: str | None = None) -> tuple[int, list, list]:
    """(root, left, right) of a BST whose node ids are their in-order ranks 0..n-1. Each subtree's
    root is a random rank, or with lean 'right' / 'left' its smallest / largest, giving a chain."""
    left, right = [None] * n, [None] * n
    root = 0  # set by the first range, which has no parent
    stack = [(0, n - 1, None, 0)]
    while stack:
        lo, hi, parent, side = stack.pop()
        if lo > hi:
            continue
        if lean == "right":
            mid = lo
        elif lean == "left":
            mid = hi
        else:
            mid = rng.randint(lo, hi)
        if parent is None:
            root = mid
        else:
            (left, right)[side][parent] = mid
        stack.append((lo, mid - 1, mid, 0))
        stack.append((mid + 1, hi, mid, 1))
    return root, left, right


def nary_tree(rng: Random, n: int, max_depth: int) -> list[int | None]:
    """LeetCode's level-order list (None ends each child group) for an n-node N-ary tree of
    height at most max_depth: a chain of max_depth, 300 or no nodes from the root, the rest
    attached at random, half of them to the root when the tree has a hub."""
    children = [[] for _ in range(n)]
    depth = [1] * n
    chain = rng.choice((max_depth, 0, 300))
    for v in range(1, chain):
        children[v - 1].append(v)
        depth[v] = depth[v - 1] + 1
    hub = rng.random() < 0.5
    for v in range(max(chain, 1), n):
        if hub and rng.random() < 0.5:
            parent = 0
        else:
            parent = rng.randrange(v)
            while depth[parent] >= max_depth:
                parent = rng.randrange(v)
        children[parent].append(v)
        depth[v] = depth[parent] + 1
    for kids in children:
        rng.shuffle(kids)
    vals = [rng.randint(0, 10**4) for _ in range(n)]
    out, queue = [vals[0], None], deque([0])
    while queue:
        node = queue.popleft()
        for child in children[node]:
            out.append(vals[child])
            queue.append(child)
        out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def primes_upto(limit: int) -> list[int]:
    """Every prime p <= limit, by the sieve of Eratosthenes."""
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = bytes(len(range(p * p, limit + 1, p)))
    return [i for i in range(limit + 1) if sieve[i]]
