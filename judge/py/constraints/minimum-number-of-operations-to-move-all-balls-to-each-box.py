"""Minimum Number of Operations to Move All Balls to Each Box: a binary string of boxes."""


def check(boxes: str) -> None:
    assert isinstance(boxes, str), "boxes is a string"
    assert 1 <= len(boxes) <= 2000, "1 <= n <= 2000"
    assert set(boxes) <= {"0", "1"}, "boxes[i] is either '0' or '1'"
