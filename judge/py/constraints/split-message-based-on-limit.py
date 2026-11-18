"""Split Message Based on Limit: a lowercase message with spaces and a limit."""


def check(message: str, limit: int) -> None:
    assert isinstance(message, str), "message is a string"
    assert 1 <= len(message) <= 10**4, "1 <= message.length <= 10^4"
    assert all(c == " " or "a" <= c <= "z" for c in message), (
        "message consists only of lowercase English letters and ' '"
    )
    assert 1 <= limit <= 10**4, "1 <= limit <= 10^4"
