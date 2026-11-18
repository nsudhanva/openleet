"""Subdomain Visit Count: count-paired domains like "9001 discuss.leetcode.com"."""


def check(cpdomains: list[str]) -> None:
    assert isinstance(cpdomains, list), "cpdomains is a list"
    assert 1 <= len(cpdomains) <= 100, "1 <= cpdomain.length <= 100"
    for s in cpdomains:
        assert isinstance(s, str) and 1 <= len(s) <= 100, "1 <= cpdomain[i].length <= 100"
        parts = s.split(" ")
        assert len(parts) == 2, "cpdomain[i] is 'rep domain'"
        rep, domain = parts
        assert rep.isascii() and rep.isdigit(), "rep is an integer"
        assert 1 <= int(rep) <= 10**4, "rep is in the range [1, 10^4]"
        labels = domain.split(".")
        assert len(labels) in (2, 3), "domain is d1.d2 or d1.d2.d3"
        assert all(x and all("a" <= c <= "z" for c in x) for x in labels), (
            "d1, d2, d3 consist of lowercase English letters"
        )
