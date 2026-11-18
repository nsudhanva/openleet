"""Find the Kth Largest Integer in the Array: digit strings and k."""


def check(nums: list[str], k: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= k <= len(nums) <= 10**4, "1 <= k <= nums.length <= 10^4"
    assert all(isinstance(s, str) and 1 <= len(s) <= 100 for s in nums), (
        "1 <= nums[i].length <= 100"
    )
    assert all(s.isascii() and s.isdigit() for s in nums), "nums[i] consists of only digits"
    assert all(s == "0" or s[0] != "0" for s in nums), "nums[i] will not have any leading zeros"
