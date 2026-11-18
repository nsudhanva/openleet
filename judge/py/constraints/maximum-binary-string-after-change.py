"""Maximum Binary String After Change: a binary string."""


def check(binary: str) -> None:
    assert 1 <= len(binary) <= 10**5, "1 <= binary.length <= 10^5"
    assert set(binary) <= {"0", "1"}, "binary consists of '0' and '1'"
