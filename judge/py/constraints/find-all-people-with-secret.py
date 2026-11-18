"""Find All People with Secret: n people, timed meetings, and the first person told."""


def check(n: int, meetings: list[list[int]], firstPerson: int) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= len(meetings) <= 10**5, "1 <= meetings.length <= 10^5"
    assert all(len(m) == 3 for m in meetings), "meetings[i].length == 3"
    assert all(0 <= m[0] <= n - 1 and 0 <= m[1] <= n - 1 for m in meetings), "0 <= xi, yi <= n - 1"
    assert all(m[0] != m[1] for m in meetings), "xi != yi"
    assert all(1 <= m[2] <= 10**5 for m in meetings), "1 <= timei <= 10^5"
    assert 1 <= firstPerson <= n - 1, "1 <= firstPerson <= n - 1"
