"""Number of Unique Good Subsequences: a binary string."""


def check(binary: str) -> None:
    assert isinstance(binary, str), "binary is a string"
    assert 1 <= len(binary) <= 10**5, "1 <= binary.length <= 10^5"
    assert set(binary) <= {"0", "1"}, "binary consists of only '0's and '1's"
