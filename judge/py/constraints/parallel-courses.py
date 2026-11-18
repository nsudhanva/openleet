"""Parallel Courses: n courses and unique [prev, next] prerequisite pairs."""


def check(n: int, relations: list[list[int]]) -> None:
    assert isinstance(relations, list), "relations is a list"
    assert 1 <= n <= 5000, "1 <= n <= 5000"
    assert 1 <= len(relations) <= 5000, "1 <= relations.length <= 5000"
    assert all(len(r) == 2 for r in relations), "relations[i].length == 2"
    assert all(1 <= a <= n and 1 <= b <= n for a, b in relations), (
        "1 <= prevCoursei, nextCoursei <= n"
    )
    assert all(a != b for a, b in relations), "prevCoursei != nextCoursei"
    assert len({(a, b) for a, b in relations}) == len(relations), "all the pairs are unique"
