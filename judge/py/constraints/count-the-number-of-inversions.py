"""Count the Number of Inversions: n and requirements [end, cnt] on permutation prefixes."""


def check(n: int, requirements: list[list[int]]) -> None:
    assert isinstance(requirements, list), "requirements is a list"
    assert 2 <= n <= 300, "2 <= n <= 300"
    assert 1 <= len(requirements) <= n, "1 <= requirements.length <= n"
    assert all(isinstance(r, list) and len(r) == 2 for r in requirements), (
        "requirements[i] = [end, cnt]"
    )
    assert all(0 <= e <= n - 1 for e, _ in requirements), "0 <= end <= n - 1"
    assert all(0 <= c <= 400 for _, c in requirements), "0 <= cnt <= 400"
    ends = [e for e, _ in requirements]
    assert n - 1 in ends, "some end == n - 1"
    assert len(set(ends)) == len(ends), "all end are unique"
