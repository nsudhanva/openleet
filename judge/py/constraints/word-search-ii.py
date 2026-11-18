"""Word Search II: a board of lowercase letters and a list of distinct lowercase words."""


def check(board: list[list[str]], words: list[str]) -> None:
    m = len(board)
    assert 1 <= m <= 12, "1 <= m <= 12"
    n = len(board[0])
    assert 1 <= n <= 12, "1 <= n <= 12"
    assert all(len(row) == n for row in board), "n == board[i].length"
    assert all(len(c) == 1 and "a" <= c <= "z" for row in board for c in row), (
        "board[i][j] is a lowercase English letter"
    )
    assert 1 <= len(words) <= 3 * 10**4, "1 <= words.length <= 3 * 10^4"
    assert all(1 <= len(w) <= 10 for w in words), "1 <= words[i].length <= 10"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] consists of lowercase English letters"
    )
    assert len(set(words)) == len(words), "all the strings of words are unique"
