"""Video Stitching: clips as [start, end] pairs and a target time."""


def check(clips: list[list[int]], time: int) -> None:
    assert 1 <= len(clips) <= 100, "1 <= clips.length <= 100"
    assert all(len(c) == 2 for c in clips), "clips[i].length == 2"
    assert all(0 <= s <= e <= 100 for s, e in clips), "0 <= starti <= endi <= 100"
    assert 1 <= time <= 100, "1 <= time <= 100"
