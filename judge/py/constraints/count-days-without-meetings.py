"""Count Days Without Meetings: number of days and [start, end] meetings."""


def check(days: int, meetings: list[list[int]]) -> None:
    assert 1 <= days <= 10**9, "1 <= days <= 10^9"
    assert 1 <= len(meetings) <= 10**5, "1 <= meetings.length <= 10^5"
    assert all(len(m) == 2 for m in meetings), "meetings[i].length == 2"
    assert all(1 <= a <= b <= days for a, b in meetings), (
        "1 <= meetings[i][0] <= meetings[i][1] <= days"
    )
