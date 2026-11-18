"""Handshakes That Don't Cross: an even number of people."""


def check(numPeople: int) -> None:
    assert 2 <= numPeople <= 1000, "2 <= numPeople <= 1000"
    assert numPeople % 2 == 0, "numPeople is even"
