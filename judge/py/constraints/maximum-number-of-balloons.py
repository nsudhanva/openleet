"""Maximum Number of Balloons: a lowercase string."""


def check(text: str) -> None:
    assert 1 <= len(text) <= 10**4, "1 <= text.length <= 10^4"
    assert all("a" <= c <= "z" for c in text), "text consists of lower case English letters only"
