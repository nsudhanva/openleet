"""Campus Bikes: worker and bike coordinates, all distinct."""


def check(workers: list[list[int]], bikes: list[list[int]]) -> None:
    n, m = len(workers), len(bikes)
    assert 1 <= n <= m <= 1000, "1 <= n <= m <= 1000"
    assert all(len(p) == 2 for p in workers), "workers[i].length == 2"
    assert all(len(p) == 2 for p in bikes), "bikes[j].length == 2"
    assert all(0 <= v < 1000 for p in workers + bikes for v in p), "0 <= xi, yi < 1000"
    locs = [tuple(p) for p in workers + bikes]
    assert len(set(locs)) == len(locs), "All worker and bike locations are unique"
