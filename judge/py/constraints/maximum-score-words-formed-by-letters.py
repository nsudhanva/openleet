"""Maximum Score Words Formed by Letters: lowercase words, single-letter tiles and 26 letter
scores."""


def check(words: list[str], letters: list[str], score: list[int]) -> None:
    assert 1 <= len(words) <= 14, "1 <= words.length <= 14"
    assert all(1 <= len(w) <= 15 for w in words), "1 <= words[i].length <= 15"
    assert 1 <= len(letters) <= 100, "1 <= letters.length <= 100"
    assert all(len(c) == 1 for c in letters), "letters[i].length == 1"
    assert len(score) == 26, "score.length == 26"
    assert all(0 <= v <= 10 for v in score), "0 <= score[i] <= 10"
    assert all("a" <= ch <= "z" for w in words for ch in w), (
        "words[i] contains only lower case English letters"
    )
    assert all("a" <= c <= "z" for c in letters), (
        "letters[i] contains only lower case English letters"
    )
