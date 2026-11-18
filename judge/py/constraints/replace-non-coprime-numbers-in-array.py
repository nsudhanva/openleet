"""Replace Non-Coprime Numbers in Array: an array of positive integers."""

from math import gcd


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    stack: list[int] = []
    for v in nums:
        while stack and gcd(stack[-1], v) > 1:
            g = gcd(stack[-1], v)
            v = stack.pop() // g * v
            assert v <= 10**8, "values in the final array are <= 10^8"
        stack.append(v)
    assert all(v <= 10**8 for v in stack), "values in the final array are <= 10^8"
