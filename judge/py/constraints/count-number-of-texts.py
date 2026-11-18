"""Count Number of Texts: a string of keypad digits 2-9."""


def check(pressedKeys: str) -> None:
    assert isinstance(pressedKeys, str), "pressedKeys is a string"
    assert 1 <= len(pressedKeys) <= 10**5, "1 <= pressedKeys.length <= 10^5"
    assert all("2" <= c <= "9" for c in pressedKeys), (
        "pressedKeys only consists of digits from '2' - '9'"
    )
