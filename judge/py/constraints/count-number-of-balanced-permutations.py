"""Count Number of Balanced Permutations: a digit string."""


def check(num: str) -> None:
    assert isinstance(num, str), "num is a string"
    assert 2 <= len(num) <= 80, "2 <= num.length <= 80"
    assert all("0" <= c <= "9" for c in num), "num consists of digits '0' to '9' only"
