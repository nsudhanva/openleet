"""Calculate Score After Performing Instructions: add/jump instructions with values."""


def check(instructions: list[str], values: list[int]) -> None:
    n = len(instructions)
    assert n == len(values), "n == instructions.length == values.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(i in ("add", "jump") for i in instructions), 'instructions[i] is "add" or "jump"'
    assert all(-(10**5) <= v <= 10**5 for v in values), "-10^5 <= values[i] <= 10^5"
