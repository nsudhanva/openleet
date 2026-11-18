"""Diameter of N-Ary Tree: an n-ary tree in level-order, groups of children split by null."""


def check(root: list[int | None]) -> None:
    assert root and root[0] is not None, "the tree has a root"
    assert len(root) == 1 or root[1] is None, "the root is followed by null"
    depths = [1]
    qi, i = 0, 2
    while i < len(root):
        assert qi < len(depths), "every group of children has a parent"
        while i < len(root) and root[i] is not None:
            depths.append(depths[qi] + 1)
            i += 1
        qi += 1
        i += 1
    assert 1 <= len(depths) <= 10**4, "the total number of nodes is between [1, 10^4]"
    assert max(depths) - 1 <= 1000, "the depth of the n-ary tree is <= 1000"
