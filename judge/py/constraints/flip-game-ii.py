"""Flip Game II: a short string of '+' and '-'."""


def check(currentState: str) -> None:
    assert 1 <= len(currentState) <= 60, "1 <= currentState.length <= 60"
    assert all(c in "+-" for c in currentState), "currentState[i] is either '+' or '-'"
    assert all(len(run) <= 20 for run in currentState.split("-")), (
        "there cannot be more than 20 consecutive '+'"
    )
