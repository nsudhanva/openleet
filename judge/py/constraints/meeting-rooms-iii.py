"""Meeting Rooms III: a room count and [start, end) meetings with unique starts."""


def check(n: int, meetings: list[list[int]]) -> None:
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert 1 <= len(meetings) <= 10**5, "1 <= meetings.length <= 10^5"
    assert all(len(m) == 2 for m in meetings), "meetings[i].length == 2"
    assert all(0 <= s < e <= 5 * 10**5 for s, e in meetings), "0 <= starti < endi <= 5 * 10^5"
    assert len({s for s, _ in meetings}) == len(meetings), "all starti are unique"
