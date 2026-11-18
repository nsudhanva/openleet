"""Pascal's Triangle: a row count."""


def check(numRows: int) -> None:
    assert isinstance(numRows, int) and 1 <= numRows <= 30, "1 <= numRows <= 30"
