"""Maximize Meeting Earnings with Idle Gaps: meetings as [start, end, revenue]."""


def check(meetings: list[list[int]]) -> None:
    assert 1 <= len(meetings) <= 10**5, "1 <= meetings.length <= 10^5"
    assert all(len(m) == 3 for m in meetings), "meetings[i] = [start, end, revenue]"
    assert all(0 <= s < e <= 10**9 for s, e, _ in meetings), "0 <= start < end <= 10^9"
    assert all(1 <= r <= 10**9 for _, _, r in meetings), "1 <= revenue <= 10^9"
