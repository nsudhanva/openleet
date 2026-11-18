"""Replace Words: a dictionary of roots and a sentence of lowercase words."""


def check(dictionary: list[str], sentence: str) -> None:
    assert 1 <= len(dictionary) <= 1000, "1 <= dictionary.length <= 1000"
    for d in dictionary:
        assert isinstance(d, str), "dictionary[i] is a string"
        assert 1 <= len(d) <= 100, "1 <= dictionary[i].length <= 100"
        assert all("a" <= c <= "z" for c in d), "dictionary[i] consists of only lower-case letters"
    assert isinstance(sentence, str), "sentence is a string"
    assert 1 <= len(sentence) <= 10**6, "1 <= sentence.length <= 10^6"
    assert all(c == " " or "a" <= c <= "z" for c in sentence), (
        "sentence consists of only lower-case letters and spaces"
    )
    assert not sentence.startswith(" ") and not sentence.endswith(" "), (
        "sentence does not have leading or trailing spaces"
    )
    words = sentence.split(" ")
    assert all(words), "every two consecutive words are separated by exactly one space"
    assert 1 <= len(words) <= 1000, "number of words in sentence is in [1, 1000]"
    assert all(1 <= len(w) <= 1000 for w in words), "length of each word is in [1, 1000]"
