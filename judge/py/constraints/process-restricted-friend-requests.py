"""Process Restricted Friend Requests: n people, restriction pairs and request pairs."""


def check(n: int, restrictions: list[list[int]], requests: list[list[int]]) -> None:
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert 0 <= len(restrictions) <= 1000, "0 <= restrictions.length <= 1000"
    assert all(isinstance(p, list) and len(p) == 2 for p in restrictions), (
        "restrictions[i].length == 2"
    )
    assert all(0 <= v <= n - 1 for p in restrictions for v in p), "0 <= xi, yi <= n - 1"
    assert all(x != y for x, y in restrictions), "xi != yi"
    assert 1 <= len(requests) <= 1000, "1 <= requests.length <= 1000"
    assert all(isinstance(p, list) and len(p) == 2 for p in requests), "requests[j].length == 2"
    assert all(0 <= v <= n - 1 for p in requests for v in p), "0 <= uj, vj <= n - 1"
    assert all(u != v for u, v in requests), "uj != vj"
