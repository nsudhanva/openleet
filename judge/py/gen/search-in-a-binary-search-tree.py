"""Search in a BST with 5000 distinct nodes: a random BST, or a 5000-deep chain (recursion
depth worst case), searching for the deepest value or an absent one."""

from _shapes import level_order

SEEDS = 3


def generate(rng):
    chain = rng.random() < 0.5
    n = 5000
    vals = rng.sample(range(1, 10**7 + 1), n)
    left, right = [None] * n, [None] * n
    if chain:
        # Chain: sorted ascending, each node is the right child of the previous one.
        vals.sort(reverse=rng.random() < 0.5)
        for i in range(n - 1):
            if vals[i + 1] > vals[i]:
                right[i] = i + 1
            else:
                left[i] = i + 1
        deepest = vals[-1]
    else:
        for i in range(1, n):
            cur = 0
            while True:
                if vals[i] < vals[cur]:
                    if left[cur] is None:
                        left[cur] = i
                        break
                    cur = left[cur]
                else:
                    if right[cur] is None:
                        right[cur] = i
                        break
                    cur = right[cur]
        deepest = vals[-1]
    present = set(vals)
    if rng.random() < 0.6:
        val = deepest
    else:
        val = rng.randint(1, 10**7)
        while val in present:
            val = rng.randint(1, 10**7)
    return {"root": level_order(vals, left, right), "val": val}
