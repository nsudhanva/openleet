"""N-ary Tree Level Order Traversal: an n-ary tree as a level-order list."""


def check(root: list) -> None:
    if not root:
        return
    assert isinstance(root, list), "root is a level-order list"
    assert root[0] is not None, "root is not null"
    assert len(root) == 1 or root[1] is None, "root is followed by null"
    depths = [1]
    i = 2
    q = 0
    while q < len(depths):
        d = depths[q]
        q += 1
        while i < len(root) and root[i] is not None:
            depths.append(d + 1)
            i += 1
        i += 1
    assert len(depths) == sum(v is not None for v in root), "tree is well formed"
    assert len(depths) <= 10**4, "the total number of nodes is between [0, 10^4]"
    assert max(depths) <= 1000, "the height of the n-ary tree is <= 1000"
