"""Excel Sheet Column Number: a column title of uppercase letters."""


def check(columnTitle: str) -> None:
    assert isinstance(columnTitle, str), "columnTitle is a string"
    assert 1 <= len(columnTitle) <= 7, "1 <= columnTitle.length <= 7"
    assert all("A" <= c <= "Z" for c in columnTitle), (
        "columnTitle consists only of uppercase letters"
    )
    assert (len(columnTitle), columnTitle) <= (7, "FXSHRXW"), (
        'columnTitle is in the range ["A", "FXSHRXW"]'
    )
