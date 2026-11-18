"""The Earliest and Latest Rounds Where Players Compete: n players and two player numbers."""


def check(n: int, firstPlayer: int, secondPlayer: int) -> None:
    assert 2 <= n <= 28, "2 <= n <= 28"
    assert 1 <= firstPlayer < secondPlayer <= n, "1 <= firstPlayer < secondPlayer <= n"
