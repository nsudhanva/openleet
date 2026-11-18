"""Find the Original Typed String II: a lowercase word and a minimum length k."""


def check(word: str, k: int) -> None:
    assert 1 <= len(word) <= 5 * 10**5, "1 <= word.length <= 5 * 10^5"
    assert all("a" <= c <= "z" for c in word), "word consists only of lowercase English letters"
    assert 1 <= k <= 2000, "1 <= k <= 2000"
