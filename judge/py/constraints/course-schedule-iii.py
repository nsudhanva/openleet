"""Course Schedule III: courses given as [duration, lastDay]."""


def check(courses: list[list[int]]) -> None:
    assert 1 <= len(courses) <= 10**4, "1 <= courses.length <= 10^4"
    assert all(len(c) == 2 for c in courses), "courses[i].length == 2"
    assert all(1 <= v <= 10**4 for c in courses for v in c), "1 <= durationi, lastDayi <= 10^4"
