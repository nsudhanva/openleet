"""Wiggle Sort II: a list of integers that can be arranged as nums[0] < nums[1] > nums[2] < ..."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 5 * 10**4, "1 <= nums.length <= 5 * 10^4"
    assert all(0 <= v <= 5000 for v in nums), "0 <= nums[i] <= 5000"
    # The classic median split finds an arrangement whenever one exists.
    s = sorted(nums)
    half = (n + 1) // 2
    res = [0] * n
    res[0::2] = s[:half][::-1]
    res[1::2] = s[half:][::-1]
    ok = all((res[i] < res[i + 1]) if i % 2 == 0 else (res[i] > res[i + 1]) for i in range(n - 1))
    assert ok, "an answer exists for the given input"
