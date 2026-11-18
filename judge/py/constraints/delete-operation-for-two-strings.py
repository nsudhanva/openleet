"""Delete Operation for Two Strings: two lowercase strings."""


def check(word1: str, word2: str) -> None:
    for w, name in ((word1, "word1"), (word2, "word2")):
        assert isinstance(w, str), f"{name} is a string"
        assert 1 <= len(w) <= 500, f"1 <= {name}.length <= 500"
        assert all("a" <= c <= "z" for c in w), f"{name} consists of lowercase English letters"
