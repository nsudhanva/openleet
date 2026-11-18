"""Design A Leaderboard: Leaderboard(), then addScore / top / reset calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args have the same non-zero length"
    assert ops[0] == "Leaderboard" and args[0] == [], "Leaderboard() comes first"
    assert len(ops) - 1 <= 1000, "there will be at most 1000 function calls"
    players: set[int] = set()
    added: set[int] = set()
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "addScore":
            assert len(a) == 2, "addScore(playerId, score)"
            assert 1 <= a[0] <= 10000, "1 <= playerId <= 10000"
            assert 1 <= a[1] <= 100, "1 <= score <= 100"
            players.add(a[0])
            added.add(a[0])
        elif op == "reset":
            assert len(a) == 1, "reset(playerId)"
            assert 1 <= a[0] <= 10000, "1 <= playerId <= 10000"
            assert a[0] in added, "the player was added to the leaderboard before reset"
            players.discard(a[0])
        elif op == "top":
            assert len(a) == 1, "top(K)"
            assert 1 <= a[0] <= 10000, "1 <= K <= 10000"
            assert a[0] <= len(players), "K is at most the current number of players"
        else:
            raise AssertionError("ops are Leaderboard, addScore, reset, top")
