"""Total Distance Traveled: litres in the main and additional fuel tanks."""


def check(mainTank: int, additionalTank: int) -> None:
    assert 1 <= mainTank <= 100, "1 <= mainTank <= 100"
    assert 1 <= additionalTank <= 100, "1 <= additionalTank <= 100"
