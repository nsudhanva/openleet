"""Remove Boxes: a list of box colors as positive integers."""


def check(boxes: list[int]) -> None:
    assert 1 <= len(boxes) <= 100, "1 <= boxes.length <= 100"
    assert all(1 <= v <= 100 for v in boxes), "1 <= boxes[i] <= 100"
