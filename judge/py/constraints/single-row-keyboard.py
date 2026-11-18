"""Single-Row Keyboard: a keyboard layout of 26 letters and a lowercase word."""


def check(keyboard: str, word: str) -> None:
    assert len(keyboard) == 26, "keyboard.length == 26"
    assert sorted(keyboard) == list("abcdefghijklmnopqrstuvwxyz"), (
        "keyboard contains each lowercase letter exactly once"
    )
    assert 1 <= len(word) <= 10**4, "1 <= word.length <= 10^4"
    assert set(word) <= set(keyboard), "word[i] is an English lowercase letter"
