"""Sequential Digits: an inclusive range low..high."""


def check(low: int, high: int) -> None:
    assert 10 <= low <= high <= 10**9, "10 <= low <= high <= 10^9"
