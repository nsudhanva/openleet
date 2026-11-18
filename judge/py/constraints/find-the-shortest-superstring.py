"""Find the Shortest Superstring: a list of unique lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 12, "1 <= words.length <= 12"
    assert all(1 <= len(w) <= 20 for w in words), "1 <= words[i].length <= 20"
    assert all(all("a" <= c <= "z" for c in w) for w in words), (
        "words[i] consists of lowercase English letters"
    )
    assert len(set(words)) == len(words), "all the strings of words are unique"
