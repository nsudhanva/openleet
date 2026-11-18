"""Next Palindrome Using Same Digits: a palindromic numeric string."""


def check(num: str) -> None:
    assert 1 <= len(num) <= 10**5, "1 <= num.length <= 10^5"
    assert num == num[::-1], "num is a palindrome"
