"""Number of Pairs of Strings With Concatenation Equal to Target: digit strings and a target."""


def _digits(s: str) -> bool:
    return all("0" <= c <= "9" for c in s)


def _no_leading_zero(s: str) -> bool:
    return not (len(s) > 1 and s[0] == "0")


def check(nums: list[str], target: str) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert all(1 <= len(s) <= 100 for s in nums), "1 <= nums[i].length <= 100"
    assert 2 <= len(target) <= 100, "2 <= target.length <= 100"
    assert all(_digits(s) for s in nums) and _digits(target), "nums[i] and target consist of digits"
    assert all(_no_leading_zero(s) for s in nums) and _no_leading_zero(target), (
        "nums[i] and target do not have leading zeros"
    )
