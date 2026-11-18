"""Check if Two Chessboard Squares Have the Same Color: two squares like "a1"."""


def check(coordinate1: str, coordinate2: str) -> None:
    assert len(coordinate1) == len(coordinate2) == 2, (
        "coordinate1.length == coordinate2.length == 2"
    )
    for c in (coordinate1, coordinate2):
        assert "a" <= c[0] <= "h", "'a' <= coordinate[0] <= 'h'"
        assert "1" <= c[1] <= "8", "'1' <= coordinate[1] <= '8'"
