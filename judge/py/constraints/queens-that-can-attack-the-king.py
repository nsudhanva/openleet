"""Queens That Can Attack the King: queen positions and a king position on an 8 x 8 board."""


def check(queens: list[list[int]], king: list[int]) -> None:
    assert isinstance(queens, list) and isinstance(king, list), "queens and king are arrays"
    assert 1 <= len(queens) < 64, "1 <= queens.length < 64"
    assert all(isinstance(q, list) and len(q) == 2 for q in queens), "queens[i].length == 2"
    assert len(king) == 2, "king.length == 2"
    assert all(0 <= v < 8 for q in queens for v in q), "0 <= xQueeni, yQueeni < 8"
    assert all(0 <= v < 8 for v in king), "0 <= xKing, yKing < 8"
    points = [tuple(q) for q in queens] + [tuple(king)]
    assert len(set(points)) == len(points), "all the given positions are unique"
