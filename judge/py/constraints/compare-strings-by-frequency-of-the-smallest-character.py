"""Compare Strings by Frequency of the Smallest Character: query and word lists."""


def check(queries: list[str], words: list[str]) -> None:
    assert 1 <= len(queries) <= 2000, "1 <= queries.length <= 2000"
    assert 1 <= len(words) <= 2000, "1 <= words.length <= 2000"
    for name, group in (("queries", queries), ("words", words)):
        for w in group:
            assert 1 <= len(w) <= 10, f"1 <= {name}[i].length <= 10"
            assert all("a" <= c <= "z" for c in w), (
                f"{name}[i][j] consist of lowercase English letters"
            )
