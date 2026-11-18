"""Determine if Two Events Have Conflict: two [start, end] events in HH:MM."""

import re


def check(event1: list[str], event2: list[str]) -> None:
    assert len(event1) == len(event2) == 2, "event1.length == event2.length == 2"
    for e in (event1, event2):
        for t in e:
            assert isinstance(t, str) and len(t) == 5, "event[i].length == 5"
            assert re.fullmatch(r"[0-9]{2}:[0-9]{2}", t), "times follow the HH:MM format"
        assert e[0] <= e[1], "startTime <= endTime"
