"""Gas Station: gas and cost per station on a circular route, with a unique answer."""

from collections import deque


def check(gas: list[int], cost: list[int]) -> None:
    n = len(gas)
    assert len(cost) == n, "n == gas.length == cost.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= v <= 10**4 for v in gas), "0 <= gas[i] <= 10^4"
    assert all(0 <= v <= 10**4 for v in cost), "0 <= cost[i] <= 10^4"
    # prefix sums over the doubled route; start i works iff min(P[i+1..i+n]) >= P[i]
    pre = [0]
    for i in range(2 * n):
        pre.append(pre[-1] + gas[i % n] - cost[i % n])
    window: deque[int] = deque()
    good = 0
    for i in range(2 * n, 0, -1):
        # window holds indices in (start, start + n], increasing values from the front
        while window and pre[window[-1]] >= pre[i]:
            window.pop()
        window.append(i)
        start = i - 1
        if start < n:
            while window[0] > start + n:
                window.popleft()
            if pre[window[0]] >= pre[start]:
                good += 1
    assert good <= 1, "the answer is unique"
