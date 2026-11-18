"""Product of Array Except Self: an array of small integers whose products fit in 32 bits."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(-30 <= v <= 30 for v in nums), "-30 <= nums[i] <= 30"
    zeros = nums.count(0)
    if zeros >= 2:
        return
    cap = 2**31
    absolute = sorted(abs(v) for v in nums if v != 0)
    # With no zero the largest answer drops the smallest value; with one zero only the zero's
    # slot is nonzero.
    rest = absolute[1:] if zeros == 0 else absolute
    product = 1
    for v in rest:
        product *= v
        assert product <= cap, "answer[i] fits in a 32-bit integer"
