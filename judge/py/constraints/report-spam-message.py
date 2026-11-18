"""Report Spam Message: two lists of lowercase words."""


def check(message: list[str], bannedWords: list[str]) -> None:
    assert 1 <= len(message) <= 10**5, "1 <= message.length <= 10^5"
    assert 1 <= len(bannedWords) <= 10**5, "1 <= bannedWords.length <= 10^5"
    for lst, name in ((message, "message"), (bannedWords, "bannedWords")):
        for w in lst:
            assert isinstance(w, str), f"{name}[i] is a string"
            assert 1 <= len(w) <= 15, f"1 <= {name}[i].length <= 15"
            assert all("a" <= c <= "z" for c in w), f"{name}[i] consists only of lowercase letters"
