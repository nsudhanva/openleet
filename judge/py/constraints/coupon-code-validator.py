"""Coupon Code Validator: parallel lists of coupon codes, business lines and active flags."""


def check(code: list[str], businessLine: list[str], isActive: list[bool]) -> None:
    n = len(code)
    assert n == len(businessLine) == len(isActive), (
        "n == code.length == businessLine.length == isActive.length"
    )
    assert 1 <= n <= 100, "1 <= n <= 100"
    for s in code + businessLine:
        assert isinstance(s, str), "strings"
        assert len(s) <= 100, "0 <= length <= 100"
        assert all(32 <= ord(c) <= 126 for c in s), "printable ASCII characters"
    assert all(isinstance(a, bool) for a in isActive), "isActive[i] is either true or false"
