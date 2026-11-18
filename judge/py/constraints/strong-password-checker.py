"""Strong Password Checker: a password of letters, digits, '.' and '!'."""


def check(password: str) -> None:
    assert isinstance(password, str), "password is a string"
    assert 1 <= len(password) <= 50, "1 <= password.length <= 50"
    assert all(c.isascii() and (c.isalnum() or c in ".!") for c in password), (
        "password consists of letters, digits, '.' or '!'"
    )
