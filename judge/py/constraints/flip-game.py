"""Flip Game: a string of '+' and '-'."""


def check(currentState: str) -> None:
    assert 1 <= len(currentState) <= 500, "1 <= currentState.length <= 500"
    assert all(c in "+-" for c in currentState), "currentState[i] is either '+' or '-'"
