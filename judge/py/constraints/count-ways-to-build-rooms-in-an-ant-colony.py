"""Count Ways to Build Rooms in an Ant Colony: prevRoom parents forming a tree rooted at 0."""


def check(prevRoom: list[int]) -> None:
    assert isinstance(prevRoom, list), "prevRoom is a list"
    n = len(prevRoom)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert prevRoom[0] == -1, "prevRoom[0] == -1"
    assert all(0 <= p < n for p in prevRoom[1:]), "0 <= prevRoom[i] < n for all 1 <= i < n"
    # every room reachable from 0: following parents from any room must end at 0
    state = [0] * n  # 0 unseen, 1 on current path, 2 reaches room 0
    state[0] = 2
    for i in range(1, n):
        path = []
        j = i
        while state[j] == 0:
            state[j] = 1
            path.append(j)
            j = prevRoom[j]
        assert state[j] == 2, "every room is reachable from room 0"
        for j in path:
            state[j] = 2
