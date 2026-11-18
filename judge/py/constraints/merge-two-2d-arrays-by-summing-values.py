"""Merge Two 2D Arrays by Summing Values: two [id, value] lists in strictly ascending id order."""


def check(nums1: list[list[int]], nums2: list[list[int]]) -> None:
    for nums in (nums1, nums2):
        assert 1 <= len(nums) <= 200, "1 <= nums.length <= 200"
        assert all(len(p) == 2 for p in nums), "nums[i].length == 2"
        assert all(1 <= v <= 1000 for p in nums for v in p), "1 <= idi, vali <= 1000"
        assert all(nums[i][0] < nums[i + 1][0] for i in range(len(nums) - 1)), (
            "ids unique and strictly ascending"
        )
