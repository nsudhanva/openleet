"""Step-By-Step Directions From a Binary Tree Node to Another: a level-order tree and two values."""


def check(root: list, startValue: int, destValue: int) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree has a root"
    nodes = [v for v in root if v is not None]
    n = len(nodes)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= n for v in nodes), "1 <= Node.val <= n"
    assert len(set(nodes)) == n, "all the values in the tree are unique"
    # level-order validity: every non-null node needs a non-null parent
    q = 0  # index of the parent being filled
    parents = [0]
    i = 1
    while i < len(root):
        assert q < len(parents), "a node has no parent in level-order list"
        for _ in range(2):
            if i < len(root):
                if root[i] is not None:
                    parents.append(i)
                i += 1
        q += 1
    assert 1 <= startValue <= n and 1 <= destValue <= n, "1 <= startValue, destValue <= n"
    assert startValue != destValue, "startValue != destValue"
    assert startValue in set(nodes) and destValue in set(nodes), (
        "startValue and destValue exist in the tree"
    )
