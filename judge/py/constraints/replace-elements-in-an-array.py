"""Replace Elements in an Array: distinct numbers and [old, new] replacement operations."""


def check(nums: list[int], operations: list[list[int]]) -> None:
    n, m = len(nums), len(operations)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= m <= 10**5, "1 <= m <= 10^5"
    assert all(isinstance(op, list) and len(op) == 2 for op in operations), (
        "operations[i].length == 2"
    )
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
    assert all(1 <= a <= 10**6 and 1 <= b <= 10**6 for a, b in operations), (
        "1 <= operations[i][0], operations[i][1] <= 10^6"
    )
    cur = set(nums)
    assert len(cur) == n, "all values of nums are distinct"
    for a, b in operations:
        assert a in cur, "operations[i][0] exists in nums when applying the i-th operation"
        assert b not in cur, "operations[i][1] not in nums when applying the i-th operation"
        cur.remove(a)
        cur.add(b)
