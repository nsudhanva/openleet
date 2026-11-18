"""Strong Password Checker II: a password of letters, digits and special characters."""


def check(password: str) -> None:
    assert isinstance(password, str), "password is a string"
    assert 1 <= len(password) <= 100, "1 <= password.length <= 100"
    assert all(c.isascii() and (c.isalnum() or c in "!@#$%^&*()-+") for c in password), (
        'password consists of letters, digits, and "!@#$%^&*()-+"'
    )
