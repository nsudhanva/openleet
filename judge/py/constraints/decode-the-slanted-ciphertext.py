"""Decode the Slanted Ciphertext: a slanted-transposition encoding and its row count."""

import string


def check(encodedText: str, rows: int) -> None:
    assert 0 <= len(encodedText) <= 10**6, "0 <= encodedText.length <= 10^6"
    assert set(encodedText) <= set(string.ascii_lowercase + " "), (
        "encodedText consists of lowercase English letters and ' ' only"
    )
    assert 1 <= rows <= 1000, "1 <= rows <= 1000"
    if not encodedText:
        return
    assert len(encodedText) % rows == 0, (
        "encodedText is a valid encoding: a full matrix of rows rows"
    )
    cols = len(encodedText) // rows
    original = []
    for j in range(cols):
        for i in range(rows):
            if j + i >= cols:
                break
            original.append(encodedText[i * cols + j + i])
    text = "".join(original).rstrip(" ")
    grid = [" "] * (rows * cols)
    last_col_used = False
    for idx, ch in enumerate(text):
        j, i = divmod(idx, rows)
        col = j + i
        assert col < cols, "encodedText is a valid encoding of some originalText"
        grid[i * cols + col] = ch
        last_col_used = last_col_used or col == cols - 1
    assert "".join(grid) == encodedText, (
        "encodedText is a valid encoding of an originalText without trailing spaces"
    )
    assert last_col_used, "the rightmost column is not empty"
