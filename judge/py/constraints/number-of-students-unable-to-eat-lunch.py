"""Number of Students Unable to Eat Lunch: students' and sandwiches' preferences, 0 or 1."""


def check(students: list[int], sandwiches: list[int]) -> None:
    assert isinstance(students, list) and isinstance(sandwiches, list), "lists"
    assert 1 <= len(students) <= 100, "1 <= students.length <= 100"
    assert 1 <= len(sandwiches) <= 100, "1 <= sandwiches.length <= 100"
    assert len(students) == len(sandwiches), "students.length == sandwiches.length"
    assert all(v in (0, 1) for v in sandwiches), "sandwiches[i] is 0 or 1"
    assert all(v in (0, 1) for v in students), "students[i] is 0 or 1"
