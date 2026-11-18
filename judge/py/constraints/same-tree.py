"""Same Tree: two binary trees in level-order lists."""


def check(p: list, q: list) -> None:
    for t in (p, q):
        assert isinstance(t, list), "a tree is a level-order list"
        assert sum(v is not None for v in t) <= 100, (
            "the number of nodes in both trees is in the range [0, 100]"
        )
        assert all(-(10**4) <= v <= 10**4 for v in t if v is not None), "-10^4 <= Node.val <= 10^4"
