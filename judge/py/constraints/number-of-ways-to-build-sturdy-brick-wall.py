"""Number of Ways to Build Sturdy Brick Wall: wall height and width and distinct brick widths."""


def check(height: int, width: int, bricks: list[int]) -> None:
    assert isinstance(bricks, list), "bricks is a list"
    assert 1 <= height <= 100, "1 <= height <= 100"
    assert 1 <= width <= 10, "1 <= width <= 10"
    assert 1 <= len(bricks) <= 10, "1 <= bricks.length <= 10"
    assert all(1 <= b <= 10 for b in bricks), "1 <= bricks[i] <= 10"
    assert len(set(bricks)) == len(bricks), "all the values of bricks are unique"
