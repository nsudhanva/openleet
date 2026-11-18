"""Maximum Average Pass Ratio: [pass, total] pairs per class and extra students."""


def check(classes: list[list[int]], extraStudents: int) -> None:
    assert 1 <= len(classes) <= 10**5, "1 <= classes.length <= 10^5"
    assert all(len(c) == 2 for c in classes), "classes[i].length == 2"
    assert all(1 <= p <= t <= 10**5 for p, t in classes), "1 <= pass_i <= total_i <= 10^5"
    assert 1 <= extraStudents <= 10**5, "1 <= extraStudents <= 10^5"
