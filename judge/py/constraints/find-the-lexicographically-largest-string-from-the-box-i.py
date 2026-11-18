"""Find the Lexicographically Largest String From the Box I: a lowercase word and a friend count."""


def check(word: str, numFriends: int) -> None:
    assert isinstance(word, str) and 1 <= len(word) <= 5 * 10**3, "1 <= word.length <= 5 * 10^3"
    assert all("a" <= c <= "z" for c in word), "word consists only of lowercase English letters"
    assert isinstance(numFriends, int) and 1 <= numFriends <= len(word), (
        "1 <= numFriends <= word.length"
    )
