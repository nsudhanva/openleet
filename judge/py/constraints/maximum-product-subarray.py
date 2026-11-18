"""Maximum Product Subarray: small integers whose subarray products fit in 32 bits."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2 * 10**4, "1 <= nums.length <= 2 * 10^4"
    assert all(-10 <= v <= 10 for v in nums), "-10 <= nums[i] <= 10"
    lo, hi = -(2**31), 2**31 - 1
    cur_max = cur_min = 1
    for v in nums:
        cands = (v, cur_max * v, cur_min * v)
        cur_max, cur_min = max(cands), min(cands)
        assert lo <= cur_min and cur_max <= hi, "subarray products fit in 32 bits"
