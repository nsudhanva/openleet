"""Long Pressed Name: two lowercase strings, name and typed."""


def check(name: str, typed: str) -> None:
    assert isinstance(name, str) and isinstance(typed, str), "name and typed are strings"
    assert 1 <= len(name) <= 1000, "1 <= name.length <= 1000"
    assert 1 <= len(typed) <= 1000, "1 <= typed.length <= 1000"
    assert all("a" <= c <= "z" for c in name + typed), (
        "name and typed consist of only lowercase English letters"
    )
