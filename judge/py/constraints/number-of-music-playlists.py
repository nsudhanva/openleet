"""Number of Music Playlists: songs n, playlist length goal, replay gap k."""


def check(n: int, goal: int, k: int) -> None:
    assert 0 <= k < n <= goal <= 100, "0 <= k < n <= goal <= 100"
