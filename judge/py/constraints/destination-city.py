"""Destination City: a list of [cityA, cityB] direct paths."""

import re


def check(paths: list[list[str]]) -> None:
    assert 1 <= len(paths) <= 100, "1 <= paths.length <= 100"
    assert all(isinstance(p, list) and len(p) == 2 for p in paths), "paths[i].length == 2"
    for a, b in paths:
        assert all(isinstance(c, str) and re.fullmatch(r"[A-Za-z ]{1,10}", c) for c in (a, b)), (
            "1 <= city.length <= 10, letters and spaces"
        )
        assert a != b, "cityAi != cityBi"
    nxt = dict(paths)
    assert len(nxt) == len(paths), "one outgoing path per city"
    assert len({b for _, b in paths}) == len(paths), "one incoming path per city"
    starts = [a for a in nxt if a not in {b for _, b in paths}]
    assert len(starts) == 1, "the paths form a line without any loop"
    city, steps = starts[0], 0
    while city in nxt:
        city = nxt[city]
        steps += 1
    assert steps == len(paths), "the graph of paths forms one line, with exactly one destination"
