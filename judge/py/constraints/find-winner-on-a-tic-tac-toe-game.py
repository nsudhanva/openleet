"""Find Winner on a Tic Tac Toe Game: the moves of a valid tic-tac-toe game."""


def check(moves: list[list[int]]) -> None:
    assert 1 <= len(moves) <= 9, "1 <= moves.length <= 9"
    assert all(len(m) == 2 for m in moves), "moves[i].length == 2"
    assert all(0 <= r <= 2 and 0 <= c <= 2 for r, c in moves), "0 <= rowi, coli <= 2"
    assert len({(r, c) for r, c in moves}) == len(moves), "no repeated elements on moves"
    lines = [[(i, j) for j in range(3)] for i in range(3)]
    lines += [[(i, j) for i in range(3)] for j in range(3)]
    lines += [[(i, i) for i in range(3)], [(i, 2 - i) for i in range(3)]]
    mine: list[set[tuple[int, int]]] = [set(), set()]
    won = False
    for i, (r, c) in enumerate(moves):
        assert not won, "moves follow the rules of tic tac toe (no moves after the game is won)"
        player = mine[i % 2]
        player.add((r, c))
        won = any(all(cell in player for cell in line) for line in lines)
