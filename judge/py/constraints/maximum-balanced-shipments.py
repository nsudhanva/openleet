"""Maximum Balanced Shipments: an array of parcel weights."""


def check(weight: list[int]) -> None:
    assert 2 <= len(weight) <= 10**5, "2 <= n <= 10^5"
    assert all(1 <= v <= 10**9 for v in weight), "1 <= weight[i] <= 10^9"
