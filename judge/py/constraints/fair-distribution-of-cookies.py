"""Fair Distribution of Cookies: bags of cookies and a number of children k."""


def check(cookies: list[int], k: int) -> None:
    assert 2 <= len(cookies) <= 8, "2 <= cookies.length <= 8"
    assert all(1 <= c <= 10**5 for c in cookies), "1 <= cookies[i] <= 10^5"
    assert 2 <= k <= len(cookies), "2 <= k <= cookies.length"
