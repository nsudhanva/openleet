"""Sudoku Solver: a 9 x 9 board of digits and '.' with exactly one solution."""


def _count_solutions(board: list[list[str]], limit: int) -> int:
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                empties.append((r, c))
            else:
                bit = 1 << int(board[r][c])
                rows[r] |= bit
                cols[c] |= bit
                boxes[r // 3 * 3 + c // 3] |= bit

    def free(r: int, c: int) -> int:
        return 0x3FE & ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3])

    def solve() -> int:
        if not empties:
            return 1
        best = min(range(len(empties)), key=lambda i: free(*empties[i]).bit_count())
        empties[best], empties[-1] = empties[-1], empties[best]
        r, c = empties.pop()
        mask = free(r, c)
        found = 0
        while mask and found < limit:
            bit = mask & -mask
            mask ^= bit
            rows[r] |= bit
            cols[c] |= bit
            boxes[r // 3 * 3 + c // 3] |= bit
            found += solve()
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[r // 3 * 3 + c // 3] &= ~bit
        empties.append((r, c))
        return found

    return solve()


def check(board: list[list[str]]) -> None:
    assert len(board) == 9, "board.length == 9"
    assert all(len(row) == 9 for row in board), "board[i].length == 9"
    assert all(ch in ".123456789" for row in board for ch in row), "board[i][j] is a digit or '.'"
    units = []
    for i in range(9):
        units.append([board[i][j] for j in range(9)])
        units.append([board[j][i] for j in range(9)])
        br, bc = i // 3 * 3, i % 3 * 3
        units.append([board[br + a][bc + b] for a in range(3) for b in range(3)])
    for u in units:
        digits = [ch for ch in u if ch != "."]
        assert len(digits) == len(set(digits)), "the givens do not repeat in a row, column or box"
    assert _count_solutions(board, 2) == 1, "the input board has exactly one solution"
