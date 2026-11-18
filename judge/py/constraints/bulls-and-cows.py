"""Bulls and Cows: two equal-length digit strings."""


def check(secret: str, guess: str) -> None:
    assert isinstance(secret, str) and isinstance(guess, str), "secret and guess are strings"
    assert 1 <= len(secret) <= 1000, "1 <= secret.length <= 1000"
    assert 1 <= len(guess) <= 1000, "1 <= guess.length <= 1000"
    assert len(secret) == len(guess), "secret.length == guess.length"
    assert (secret + guess).isascii() and (secret + guess).isdigit(), "digits only"
