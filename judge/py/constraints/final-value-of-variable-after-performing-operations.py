"""Final Value of Variable After Performing Operations: increment and decrement strings."""


def check(operations: list[str]) -> None:
    assert 1 <= len(operations) <= 100, "1 <= operations.length <= 100"
    assert all(o in ("++X", "X++", "--X", "X--") for o in operations), (
        'operations[i] is either "++X", "X++", "--X", or "X--"'
    )
