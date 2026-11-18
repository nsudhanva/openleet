"""Total Characters in String After Transformations II: a lowercase string, t, and 26 expansion
lengths."""


def check(s: str, t: int, nums: list[int]) -> None:
    assert isinstance(s, str) and 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
    assert 1 <= t <= 10**9, "1 <= t <= 10^9"
    assert len(nums) == 26, "nums.length == 26"
    assert all(1 <= x <= 25 for x in nums), "1 <= nums[i] <= 25"
