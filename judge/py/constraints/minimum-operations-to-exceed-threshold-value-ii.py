"""Minimum Operations to Exceed Threshold Value II: positive integers and a threshold k."""

import heapq


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 2 <= len(nums) <= 2 * 10**5, "2 <= nums.length <= 2 * 10^5"
    assert all(1 <= x <= 10**9 for x in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
    heap = list(nums)
    heapq.heapify(heap)
    while heap[0] < k:
        assert len(heap) >= 2, "an answer always exists"
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        heapq.heappush(heap, min(x * 2 + y, k))
