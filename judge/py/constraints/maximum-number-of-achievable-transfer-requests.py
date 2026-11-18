"""Maximum Number of Achievable Transfer Requests: n buildings and [from, to] requests."""


def check(n: int, requests: list[list[int]]) -> None:
    assert 1 <= n <= 20, "1 <= n <= 20"
    assert 1 <= len(requests) <= 16, "1 <= requests.length <= 16"
    assert all(len(r) == 2 for r in requests), "requests[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in requests), "0 <= from_i, to_i < n"
