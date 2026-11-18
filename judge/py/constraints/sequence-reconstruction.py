"""Sequence Reconstruction: a permutation of 1..n and unique subsequences of it."""


def check(nums: list[int], sequences: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert sorted(nums) == list(range(1, n + 1)), "nums is a permutation of [1, n]"
    assert 1 <= len(sequences) <= 10**4, "1 <= sequences.length <= 10^4"
    assert all(isinstance(s, list) and 1 <= len(s) <= 10**4 for s in sequences), (
        "1 <= sequences[i].length <= 10^4"
    )
    assert 1 <= sum(len(s) for s in sequences) <= 10**5, "1 <= sum(sequences[i].length) <= 10^5"
    assert all(1 <= v <= n for s in sequences for v in s), "1 <= sequences[i][j] <= n"
    assert len({tuple(s) for s in sequences}) == len(sequences), (
        "all the arrays of sequences are unique"
    )
    pos = {v: i for i, v in enumerate(nums)}
    assert all(pos[s[j]] < pos[s[j + 1]] for s in sequences for j in range(len(s) - 1)), (
        "sequences[i] is a subsequence of nums"
    )
