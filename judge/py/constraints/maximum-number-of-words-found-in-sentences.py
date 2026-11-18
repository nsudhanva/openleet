"""Maximum Number of Words Found in Sentences: sentences of lowercase words."""


def check(sentences: list[str]) -> None:
    assert 1 <= len(sentences) <= 100, "1 <= sentences.length <= 100"
    for s in sentences:
        assert 1 <= len(s) <= 100, "1 <= sentences[i].length <= 100"
        assert all(c == " " or "a" <= c <= "z" for c in s), "only lowercase letters and ' '"
        assert s == s.strip(" "), "no leading or trailing spaces"
        assert "  " not in s, "words are separated by a single space"
