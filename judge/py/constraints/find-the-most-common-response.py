"""Find the Most Common Response: lists of lowercase-word survey responses."""


def check(responses: list[list[str]]) -> None:
    assert 1 <= len(responses) <= 1000, "1 <= responses.length <= 1000"
    assert all(1 <= len(r) <= 1000 for r in responses), "1 <= responses[i].length <= 1000"
    assert all(1 <= len(w) <= 10 for r in responses for w in r), "1 <= responses[i][j].length <= 10"
    assert all("a" <= c <= "z" for r in responses for w in r for c in w), (
        "responses[i][j] consists of only lowercase English letters"
    )
