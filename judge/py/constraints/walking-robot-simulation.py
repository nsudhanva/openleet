"""Walking Robot Simulation: robot commands and obstacle points."""


def check(commands: list[int], obstacles: list[list[int]]) -> None:
    assert 1 <= len(commands) <= 10**4, "1 <= commands.length <= 10^4"
    assert all(c in (-2, -1) or 1 <= c <= 9 for c in commands), (
        "commands[i] is either -2, -1, or an integer in the range [1, 9]"
    )
    assert 0 <= len(obstacles) <= 10**4, "0 <= obstacles.length <= 10^4"
    assert all(len(o) == 2 for o in obstacles), "obstacles[i].length == 2"
    assert all(-3 * 10**4 <= v <= 3 * 10**4 for o in obstacles for v in o), (
        "-3 * 10^4 <= xi, yi <= 3 * 10^4"
    )
