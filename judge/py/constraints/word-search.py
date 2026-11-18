"""Word Search: a board of letters and a word."""


def _letter(c: str) -> bool:
    return len(c) == 1 and c.isascii() and c.isalpha()


def check(board: list[list[str]], word: str) -> None:
    m = len(board)
    assert 1 <= m <= 6, "1 <= m <= 6"
    n = len(board[0])
    assert 1 <= n <= 6, "1 <= n <= 6"
    assert all(len(row) == n for row in board), "n = board[i].length"
    assert 1 <= len(word) <= 15, "1 <= word.length <= 15"
    assert all(_letter(c) for row in board for c in row), (
        "board consists of only lowercase and uppercase English letters"
    )
    assert all(_letter(c) for c in word), (
        "word consists of only lowercase and uppercase English letters"
    )
