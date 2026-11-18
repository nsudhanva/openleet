"""1-bit and 2-bit Characters: a list of bits."""


def check(bits: list[int]) -> None:
    assert 1 <= len(bits) <= 1000, "1 <= bits.length <= 1000"
    assert all(b in (0, 1) for b in bits), "bits[i] is either 0 or 1"
