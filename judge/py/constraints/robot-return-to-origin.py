"""Robot Return to Origin: a string of 'U', 'D', 'L' and 'R' moves."""


def check(moves: str) -> None:
    assert isinstance(moves, str), "moves is a string"
    assert 1 <= len(moves) <= 2 * 10**4, "1 <= moves.length <= 2 * 10^4"
    assert all(c in "UDLR" for c in moves), "moves only contains 'U', 'D', 'L' and 'R'"
