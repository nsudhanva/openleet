"""Check if Word Can Be Placed In Crossword: an m x n board of ' ', '#' and letters, and a word."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(board: list[list[str]], word: str) -> None:
    m = len(board)
    assert m >= 1, "m >= 1"
    n = len(board[0])
    assert all(len(row) == n for row in board), "n == board[i].length"
    assert 1 <= m * n <= 2 * 10**5, "1 <= m * n <= 2 * 10^5"
    assert all(c in (" ", "#") or c in LOWER for row in board for c in row), (
        "board[i][j] will be ' ', '#', or a lowercase English letter"
    )
    assert 1 <= len(word) <= max(m, n), "1 <= word.length <= max(m, n)"
    assert set(word) <= LOWER, "word will contain only lowercase English letters"
