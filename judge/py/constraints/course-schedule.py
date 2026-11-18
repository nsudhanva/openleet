"""Course Schedule: numCourses and unique prerequisite pairs [a, b]."""


def check(numCourses: int, prerequisites: list[list[int]]) -> None:
    assert 1 <= numCourses <= 2000, "1 <= numCourses <= 2000"
    assert 0 <= len(prerequisites) <= 5000, "0 <= prerequisites.length <= 5000"
    assert all(len(p) == 2 for p in prerequisites), "prerequisites[i].length == 2"
    assert all(0 <= v < numCourses for p in prerequisites for v in p), "0 <= ai, bi < numCourses"
    assert len({tuple(p) for p in prerequisites}) == len(prerequisites), (
        "all the pairs prerequisites[i] are unique"
    )
