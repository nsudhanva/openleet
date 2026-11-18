"""Robot Bounded In Circle: a string of 'G', 'L' and 'R' instructions."""


def check(instructions: str) -> None:
    assert isinstance(instructions, str), "instructions is a string"
    assert 1 <= len(instructions) <= 100, "1 <= instructions.length <= 100"
    assert all(c in "GLR" for c in instructions), "instructions[i] is 'G', 'L' or 'R'"
