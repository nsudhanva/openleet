"""UTF-8 Validation: a list of byte values."""


def check(data: list[int]) -> None:
    assert isinstance(data, list), "data is a list"
    assert 1 <= len(data) <= 2 * 10**4, "1 <= data.length <= 2 * 10^4"
    assert all(isinstance(v, int) and 0 <= v <= 255 for v in data), "0 <= data[i] <= 255"
