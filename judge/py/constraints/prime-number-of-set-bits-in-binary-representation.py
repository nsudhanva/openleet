"""Prime Number of Set Bits in Binary Representation: an inclusive integer range."""


def check(left: int, right: int) -> None:
    assert 1 <= left <= right <= 10**6, "1 <= left <= right <= 10^6"
    assert 0 <= right - left <= 10**4, "0 <= right - left <= 10^4"
