"""Binary Watch: number of LEDs turned on."""


def check(turnedOn: int) -> None:
    assert 0 <= turnedOn <= 10, "0 <= turnedOn <= 10"
