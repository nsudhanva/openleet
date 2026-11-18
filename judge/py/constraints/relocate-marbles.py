"""Relocate Marbles: marble positions plus parallel lists of move sources and destinations."""


def check(nums: list[int], moveFrom: list[int], moveTo: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert 1 <= len(moveFrom) <= 10**5, "1 <= moveFrom.length <= 10^5"
    assert len(moveFrom) == len(moveTo), "moveFrom.length == moveTo.length"
    assert all(1 <= v <= 10**9 for v in nums + moveFrom + moveTo), (
        "1 <= nums[i], moveFrom[i], moveTo[i] <= 10^9"
    )
    occupied = set(nums)
    for src, dst in zip(moveFrom, moveTo, strict=True):
        assert src in occupied, "there is at least a marble in moveFrom[i] at the moment of move i"
        occupied.discard(src)
        occupied.add(dst)
