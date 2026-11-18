"""Masking Personal Information: an email address or a phone number."""

_SEPARATORS = set("+-() ")


def _letters(text: str) -> bool:
    return all(c.isascii() and c.isalpha() for c in text)


def check(s: str) -> None:
    if "@" in s:
        assert 8 <= len(s) <= 40, "email: 8 <= s.length <= 40"
        assert s.count("@") == 1 and s.count(".") == 1, "exactly one '@' and one '.'"
        name, domain = s.split("@")
        assert len(name) >= 2 and _letters(name), "name: at least two English letters"
        dot = domain.find(".")
        assert 0 < dot < len(domain) - 1, "domain: '.' in the middle"
        assert _letters(domain.replace(".", "")), "domain: English letters and a dot"
    else:
        assert 10 <= len(s) <= 20, "phone: 10 <= s.length <= 20"
        assert all(c in "0123456789" or c in _SEPARATORS for c in s), "phone: ASCII digits"
        assert 10 <= sum(c in "0123456789" for c in s) <= 13, "phone has 10-13 digits"
