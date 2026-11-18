"""Unique Email Addresses: a list of email strings."""

ALLOWED = set("abcdefghijklmnopqrstuvwxyz+.@")


def check(emails: list[str]) -> None:
    assert isinstance(emails, list), "emails is a list"
    assert 1 <= len(emails) <= 100, "1 <= emails.length <= 100"
    assert all(isinstance(e, str) for e in emails), "emails[i] is a string"
    for e in emails:
        assert 1 <= len(e) <= 100, "1 <= emails[i].length <= 100"
        assert set(e) <= ALLOWED, "emails[i] consist of lowercase letters, '+', '.' and '@'"
        assert e.count("@") == 1, "each emails[i] contains exactly one '@'"
        local, domain = e.split("@")
        assert local and domain, "local and domain names are non-empty"
        assert not local.startswith("+"), "local names do not start with '+'"
        assert domain.endswith(".com"), "domain names end with '.com'"
        assert len(domain) > 4, "domain names have at least one character before '.com'"
