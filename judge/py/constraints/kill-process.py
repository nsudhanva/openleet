"""Kill Process: process ids, parent ids (0 for the root) and the process to kill."""


def check(pid: list[int], ppid: list[int], kill: int) -> None:
    n = len(pid)
    assert len(ppid) == n, "n == pid.length == ppid.length"
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert all(1 <= v <= 5 * 10**4 for v in pid), "1 <= pid[i] <= 5 * 10^4"
    assert all(0 <= v <= 5 * 10**4 for v in ppid), "0 <= ppid[i] <= 5 * 10^4"
    assert sum(v == 0 for v in ppid) == 1, "only one process has no parent"
    assert len(set(pid)) == n, "all the values of pid are unique"
    assert kill in set(pid), "kill is guaranteed to be in pid"
