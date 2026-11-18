"""Construct the Minimum Bitwise Array I: an array of small primes."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(2 <= x <= 1000 for x in nums), "2 <= nums[i] <= 1000"
    assert all(all(x % d for d in range(2, int(x**0.5) + 1)) for x in nums), (
        "nums[i] is a prime number"
    )
