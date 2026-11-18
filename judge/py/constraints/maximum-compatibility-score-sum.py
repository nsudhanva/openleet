"""Maximum Compatibility Score Sum: m students and m mentors with n binary answers each."""


def check(students: list[list[int]], mentors: list[list[int]]) -> None:
    m = len(students)
    assert m == len(mentors), "m == students.length == mentors.length"
    assert 1 <= m <= 8, "1 <= m <= 8"
    n = len(students[0])
    assert 1 <= n <= 8, "1 <= n <= 8"
    assert all(len(r) == n for r in students), "n == students[i].length"
    assert all(len(r) == n for r in mentors), "n == mentors[j].length"
    assert all(v in (0, 1) for r in students for v in r), "students[i][k] is 0 or 1"
    assert all(v in (0, 1) for r in mentors for v in r), "mentors[j][k] is 0 or 1"
