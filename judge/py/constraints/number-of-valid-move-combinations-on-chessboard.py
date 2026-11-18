"""Number of Valid Move Combinations On Chessboard: piece names and their 1-based positions."""


def check(pieces: list[str], positions: list[list[int]]) -> None:
    assert isinstance(pieces, list) and isinstance(positions, list), "lists"
    n = len(pieces)
    assert n == len(positions), "n == pieces.length == positions.length"
    assert 1 <= n <= 4, "1 <= n <= 4"
    assert all(p in ("rook", "queen", "bishop") for p in pieces), (
        'pieces only contains "rook", "queen", and "bishop"'
    )
    assert pieces.count("queen") <= 1, "at most one queen"
    assert all(isinstance(q, list) and len(q) == 2 for q in positions), "positions[i] has 2 values"
    assert all(1 <= v <= 8 for q in positions for v in q), "1 <= ri, ci <= 8"
    assert len({tuple(q) for q in positions}) == n, "each positions[i] is distinct"
