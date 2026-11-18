"""Get Watched Videos by Your Friends: video lists, a friendship graph, a person and a level."""


def check(watchedVideos: list[list[str]], friends: list[list[int]], id: int, level: int) -> None:
    n = len(watchedVideos)
    assert n == len(friends), "n == watchedVideos.length == friends.length"
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert all(1 <= len(w) <= 100 for w in watchedVideos), "1 <= watchedVideos[i].length <= 100"
    assert all(1 <= len(s) <= 8 for w in watchedVideos for s in w), (
        "1 <= watchedVideos[i][j].length <= 8"
    )
    assert all(len(f) < n for f in friends), "0 <= friends[i].length < n"
    assert all(0 <= j < n for f in friends for j in f), "0 <= friends[i][j] < n"
    assert 0 <= id < n, "0 <= id < n"
    assert 1 <= level < n, "1 <= level < n"
    sets = [set(f) for f in friends]
    assert all(i in sets[j] for i in range(n) for j in sets[i]), (
        "if friends[i] contains j, then friends[j] contains i"
    )
