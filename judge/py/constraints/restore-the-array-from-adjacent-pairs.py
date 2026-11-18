"""Restore the Array From Adjacent Pairs: the n - 1 adjacent pairs of unique integers."""


def check(adjacentPairs: list[list[int]]) -> None:
    n = len(adjacentPairs) + 1
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(len(p) == 2 for p in adjacentPairs), "adjacentPairs[i].length == 2"
    assert all(-(10**5) <= v <= 10**5 for p in adjacentPairs for v in p), "-10^5 <= ui, vi <= 10^5"
    adj: dict[int, list[int]] = {}
    for u, v in adjacentPairs:
        assert u != v, "the pairs come from an array of unique elements"
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    assert len(adj) == n, "nums has n unique elements"
    assert all(len(x) <= 2 for x in adj.values()), "every element has at most two neighbours"
    ends = [k for k, x in adj.items() if len(x) == 1]
    assert len(ends) == 2, "the pairs form a single path"
    prev, cur, seen = None, ends[0], 1
    while True:
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            break
        assert len(nxt) == 1, "there exists some nums that has adjacentPairs as its pairs"
        prev, cur = cur, nxt[0]
        seen += 1
        assert seen <= n, "there exists some nums that has adjacentPairs as its pairs"
    assert seen == n, "there exists some nums that has adjacentPairs as its pairs"
