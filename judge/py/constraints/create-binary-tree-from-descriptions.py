"""Create Binary Tree From Descriptions: [parent, child, isLeft] edges of one valid tree."""


def check(descriptions: list[list[int]]) -> None:
    assert 1 <= len(descriptions) <= 10**4, "1 <= descriptions.length <= 10^4"
    assert all(len(d) == 3 for d in descriptions), "descriptions[i].length == 3"
    assert all(1 <= p <= 10**5 and 1 <= c <= 10**5 for p, c, _ in descriptions), (
        "1 <= parenti, childi <= 10^5"
    )
    assert all(left in (0, 1) for _, _, left in descriptions), "0 <= isLefti <= 1"
    kids: dict[int, list[int]] = {}
    children = set()
    slots = set()
    for p, c, left in descriptions:
        assert c not in children, "valid tree: each node has at most one parent"
        children.add(c)
        assert (p, left) not in slots, (
            "valid tree: each node has at most one left and one right child"
        )
        slots.add((p, left))
        kids.setdefault(p, []).append(c)
    roots = set(kids) - children
    assert len(roots) == 1, "valid tree: exactly one root"
    stack = list(roots)
    seen = 0
    while stack:
        v = stack.pop()
        seen += 1
        stack.extend(kids.get(v, []))
    assert seen == len(descriptions) + 1, "valid tree: connected and acyclic"
