"""Open the Lock: four-digit deadend strings and a four-digit target not among them."""


def check(deadends: list[str], target: str) -> None:
    assert 1 <= len(deadends) <= 500, "1 <= deadends.length <= 500"
    assert all(isinstance(d, str) and len(d) == 4 for d in deadends), "deadends[i].length == 4"
    assert isinstance(target, str) and len(target) == 4, "target.length == 4"
    assert all(d.isascii() and d.isdigit() for d in deadends), "deadends[i] consists of digits only"
    assert target.isascii() and target.isdigit(), "target consists of digits only"
    assert target not in set(deadends), "target will not be in the list deadends"
