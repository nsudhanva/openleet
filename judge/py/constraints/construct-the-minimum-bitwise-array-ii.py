"""Construct the Minimum Bitwise Array II: a list of primes."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(isinstance(v, int) for v in nums), "nums[i] is an integer"
    assert all(2 <= v <= 10**9 for v in nums), "2 <= nums[i] <= 10^9"
    for v in nums:
        assert is_prime(v), "nums[i] is a prime number"


def is_prime(v: int) -> bool:
    if v < 2:
        return False
    if v % 2 == 0:
        return v == 2
    i = 3
    while i * i <= v:
        if v % i == 0:
            return False
        i += 2
    return True
