"""Bus Routes: bus routes as stop lists, a source and a target stop."""


def check(routes: list[list[int]], source: int, target: int) -> None:
    assert 1 <= len(routes) <= 500, "1 <= routes.length <= 500"
    assert all(isinstance(r, list) for r in routes), "routes is a list of lists"
    assert all(1 <= len(r) <= 10**5 for r in routes), "1 <= routes[i].length <= 10^5"
    assert all(len(set(r)) == len(r) for r in routes), "All the values of routes[i] are unique"
    assert sum(len(r) for r in routes) <= 10**5, "sum(routes[i].length) <= 10^5"
    assert all(0 <= s < 10**6 for r in routes for s in r), "0 <= routes[i][j] < 10^6"
    assert 0 <= source < 10**6, "0 <= source < 10^6"
    assert 0 <= target < 10**6, "0 <= target < 10^6"
