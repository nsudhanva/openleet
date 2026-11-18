"""Recover a Tree From Preorder Traversal: dashes and values of a preorder DFS."""

import re


def check(traversal: str) -> None:
    assert isinstance(traversal, str), "traversal is a string"
    assert re.fullmatch(r"[0-9]+(-+[0-9]+)*", traversal), "dashes then value, per node"
    nodes = [(len(d), int(v)) for d, v in re.findall(r"(-*)([0-9]+)", traversal)]
    assert 1 <= len(nodes) <= 1000, "number of nodes in [1, 1000]"
    assert all(1 <= v <= 10**9 for _, v in nodes), "1 <= Node.val <= 10^9"
    assert nodes[0][0] == 0, "the root has depth 0"
    children = [0]  # children[d] = children seen so far of the latest node at depth d
    for depth, _ in nodes[1:]:
        assert 1 <= depth <= len(children), "a node's depth is its parent's depth + 1"
        del children[depth:]
        children[depth - 1] += 1
        assert children[depth - 1] <= 2, "a binary tree node has at most two children"
        children.append(0)
