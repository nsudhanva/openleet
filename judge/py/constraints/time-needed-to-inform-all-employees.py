"""Time Needed to Inform All Employees: a management tree given by manager[] and informTime[]."""


def check(n: int, headID: int, manager: list[int], informTime: list[int]) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 0 <= headID < n, "0 <= headID < n"
    assert len(manager) == n, "manager.length == n"
    assert len(informTime) == n, "informTime.length == n"
    assert all(0 <= m < n or (i == headID and m == -1) for i, m in enumerate(manager)), (
        "0 <= manager[i] < n"
    )
    assert manager[headID] == -1, "manager[headID] == -1"
    assert all(0 <= t <= 1000 for t in informTime), "0 <= informTime[i] <= 1000"
    children = [[] for _ in range(n)]
    for i, m in enumerate(manager):
        if i != headID:
            children[m].append(i)
    assert all(informTime[i] == 0 for i in range(n) if not children[i]), (
        "informTime[i] == 0 if employee i has no subordinates"
    )
    seen = 1
    stack = [headID]
    while stack:
        for c in children[stack.pop()]:
            seen += 1
            stack.append(c)
            assert seen <= n, "all the employees can be informed"
    assert seen == n, "all the employees can be informed"
