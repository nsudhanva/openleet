"""Campus Bikes II: worker and bike coordinates, all distinct."""


def check(workers: list[list[int]], bikes: list[list[int]]) -> None:
    n, m = len(workers), len(bikes)
    assert 1 <= n <= m <= 10, "1 <= n <= m <= 10"
    assert all(len(p) == 2 for p in workers), "workers[i].length == 2"
    assert all(len(p) == 2 for p in bikes), "bikes[i].length == 2"
    assert all(0 <= v < 1000 for p in workers + bikes for v in p), "0 <= coordinates < 1000"
    locs = [tuple(p) for p in workers + bikes]
    assert len(set(locs)) == len(locs), "All the workers and the bikes locations are unique"
