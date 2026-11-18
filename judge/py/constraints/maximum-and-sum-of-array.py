"""Maximum AND Sum of Array: small numbers and a slot count."""


def check(nums: list[int], numSlots: int) -> None:
    assert 1 <= numSlots <= 9, "1 <= numSlots <= 9"
    assert 1 <= len(nums) <= 2 * numSlots, "1 <= n <= 2 * numSlots"
    assert all(1 <= v <= 15 for v in nums), "1 <= nums[i] <= 15"
