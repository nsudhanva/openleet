"""Maximum Number of Words You Can Type: text of lowercase words and distinct broken letters."""


def check(text: str, brokenLetters: str) -> None:
    assert 1 <= len(text) <= 10**4, "1 <= text.length <= 10^4"
    assert 0 <= len(brokenLetters) <= 26, "0 <= brokenLetters.length <= 26"
    assert all(c == " " or "a" <= c <= "z" for c in text), "words of lowercase English letters"
    assert text == text.strip(" "), "no leading or trailing spaces"
    assert "  " not in text, "words are separated by a single space"
    assert all("a" <= c <= "z" for c in brokenLetters), "brokenLetters is lowercase letters"
    assert len(set(brokenLetters)) == len(brokenLetters), "brokenLetters are distinct"
