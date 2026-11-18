"""Find the Divisibility Array of a String: a digit string and a divisor m."""


def check(word: str, m: int) -> None:
    assert isinstance(word, str), "word is a string"
    assert 1 <= len(word) <= 10**5, "1 <= n <= 10^5, word.length == n"
    assert all("0" <= c <= "9" for c in word), "word consists of digits from 0 to 9"
    assert 1 <= m <= 10**9, "1 <= m <= 10^9"
