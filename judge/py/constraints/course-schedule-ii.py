"""Course Schedule II: numCourses and distinct prerequisite pairs [a, b] with a != b."""


def check(numCourses: int, prerequisites: list[list[int]]) -> None:
    assert 1 <= numCourses <= 2000, "1 <= numCourses <= 2000"
    assert 0 <= len(prerequisites) <= numCourses * (numCourses - 1), (
        "0 <= prerequisites.length <= numCourses * (numCourses - 1)"
    )
    assert all(len(p) == 2 for p in prerequisites), "prerequisites[i].length == 2"
    assert all(0 <= v < numCourses for p in prerequisites for v in p), "0 <= ai, bi < numCourses"
    assert all(a != b for a, b in prerequisites), "ai != bi"
    assert len({tuple(p) for p in prerequisites}) == len(prerequisites), (
        "all the pairs [ai, bi] are distinct"
    )
