"""Find the Maximum Sequence Value of Array: small integers and a half-length k."""


def check(nums: list[int], k: int) -> None:
    assert 2 <= len(nums) <= 400, "2 <= nums.length <= 400"
    assert all(1 <= v < 2**7 for v in nums), "1 <= nums[i] < 2^7"
    assert k >= 1 and 2 * k <= len(nums), "1 <= k <= nums.length / 2"
