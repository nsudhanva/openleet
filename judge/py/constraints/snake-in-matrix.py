"""Snake in Matrix: grid size n and a list of moves that stay inside the grid."""

_D = {"UP": (-1, 0), "RIGHT": (0, 1), "DOWN": (1, 0), "LEFT": (0, -1)}


def check(n: int, commands: list[str]) -> None:
    assert 2 <= n <= 10, "2 <= n <= 10"
    assert 1 <= len(commands) <= 100, "1 <= commands.length <= 100"
    assert all(c in _D for c in commands), 'commands consists only of "UP", "RIGHT", "DOWN", "LEFT"'
    r = c = 0
    for cmd in commands:
        dr, dc = _D[cmd]
        r, c = r + dr, c + dc
        assert 0 <= r < n and 0 <= c < n, "the snake does not move outside the boundaries"
