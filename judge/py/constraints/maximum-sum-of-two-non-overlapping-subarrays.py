"""Maximum Sum of Two Non-Overlapping Subarrays: an array and two subarray lengths."""


def check(nums: list[int], firstLen: int, secondLen: int) -> None:
    assert 1 <= firstLen <= 1000 and 1 <= secondLen <= 1000, "1 <= firstLen, secondLen <= 1000"
    assert 2 <= firstLen + secondLen <= 1000, "2 <= firstLen + secondLen <= 1000"
    assert firstLen + secondLen <= len(nums) <= 1000, "firstLen + secondLen <= nums.length <= 1000"
    assert all(0 <= v <= 1000 for v in nums), "0 <= nums[i] <= 1000"
