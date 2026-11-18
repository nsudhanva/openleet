"""Break a Palindrome: a palindromic lowercase string."""

from string import ascii_lowercase


def check(palindrome: str) -> None:
    assert 1 <= len(palindrome) <= 1000, "1 <= palindrome.length <= 1000"
    assert set(palindrome) <= set(ascii_lowercase), (
        "palindrome consists of only lowercase English letters"
    )
    assert palindrome == palindrome[::-1], "palindrome is a palindrome"
