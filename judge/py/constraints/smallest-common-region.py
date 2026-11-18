"""Smallest Common Region: region lists (parent first, then children) and two regions."""


def check(regions: list[list[str]], region1: str, region2: str) -> None:
    assert 2 <= len(regions) <= 10**4, "2 <= regions.length <= 10^4"
    assert all(2 <= len(r) <= 20 for r in regions), "2 <= regions[i].length <= 20"
    names = set()
    for r in regions:
        for name in r:
            assert isinstance(name, str) and 1 <= len(name) <= 20, "1 <= regions[i][j].length <= 20"
            names.add(name)
    assert 1 <= len(region1) <= 20 and 1 <= len(region2) <= 20, (
        "1 <= region1.length, region2.length <= 20"
    )
    assert region1 != region2, "region1 != region2"
    parent: dict[str, str] = {}
    children: dict[str, list[str]] = {}
    for r in regions:
        children.setdefault(r[0], []).extend(r[1:])
        for c in r[1:]:
            assert c not in parent, "a region cannot be directly contained in more than one region"
            parent[c] = r[0]
    roots = [n for n in names if n not in parent]
    assert len(roots) == 1, "exactly one region contains all the others"
    seen = {roots[0]}
    stack = [roots[0]]
    while stack:
        for c in children.get(stack.pop(), []):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    assert len(seen) == len(names), "one region contains all the others"
    assert region1 in names and region2 in names, "region1 and region2 are regions"
