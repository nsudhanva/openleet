"""Valid Arrangement of Pairs: distinct directed edges that admit an Eulerian path."""


def check(pairs: list[list[int]]) -> None:
    assert isinstance(pairs, list), "pairs is a list"
    assert 1 <= len(pairs) <= 10**5, "1 <= pairs.length <= 10^5"
    assert all(isinstance(p, list) and len(p) == 2 for p in pairs), "pairs[i].length == 2"
    assert all(0 <= a <= 10**9 and 0 <= b <= 10**9 for a, b in pairs), "0 <= starti, endi <= 10^9"
    assert all(a != b for a, b in pairs), "starti != endi"
    assert len({(a, b) for a, b in pairs}) == len(pairs), "no two pairs are exactly the same"
    diff: dict[int, int] = {}
    parent: dict[int, int] = {}

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for a, b in pairs:
        diff[a] = diff.get(a, 0) + 1
        diff[b] = diff.get(b, 0) - 1
        parent.setdefault(a, a)
        parent.setdefault(b, b)
        parent[find(a)] = find(b)
    nonzero = [d for d in diff.values() if d != 0]
    assert all(d in (1, -1) for d in nonzero) and sorted(nonzero) in ([], [-1, 1]), (
        "there exists a valid arrangement of pairs"
    )
    assert len({find(x) for x in parent}) == 1, "there exists a valid arrangement of pairs"
