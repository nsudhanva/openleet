"""Count Vowel Strings in Ranges: lowercase words and [li, ri] queries."""


def check(words: list[str], queries: list[list[int]]) -> None:
    assert isinstance(words, list) and isinstance(queries, list), "words, queries are lists"
    assert 1 <= len(words) <= 10**5, "1 <= words.length <= 10^5"
    assert all(isinstance(w, str) and 1 <= len(w) <= 40 for w in words), (
        "1 <= words[i].length <= 40"
    )
    assert all(w.isascii() and w.islower() for w in words), (
        "words[i] consists only of lowercase English letters"
    )
    assert sum(len(w) for w in words) <= 3 * 10**5, "sum(words[i].length) <= 3 * 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(isinstance(q, list) and len(q) == 2 for q in queries), "queries[i] = [li, ri]"
    assert all(0 <= lo <= hi < len(words) for lo, hi in queries), "0 <= li <= ri < words.length"
