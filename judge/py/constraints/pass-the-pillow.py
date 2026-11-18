"""Pass the Pillow: n people in a line and a number of seconds."""


def check(n: int, time: int) -> None:
    assert isinstance(n, int) and 2 <= n <= 1000, "2 <= n <= 1000"
    assert isinstance(time, int) and 1 <= time <= 1000, "1 <= time <= 1000"
