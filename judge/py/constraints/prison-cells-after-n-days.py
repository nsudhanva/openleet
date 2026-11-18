"""Prison Cells After N Days: eight cells of 0 or 1 and a day count."""


def check(cells: list[int], n: int) -> None:
    assert isinstance(cells, list), "cells is an array"
    assert len(cells) == 8, "cells.length == 8"
    assert all(c in (0, 1) for c in cells), "cells[i] is either 0 or 1"
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
