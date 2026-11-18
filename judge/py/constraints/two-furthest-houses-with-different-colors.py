"""Two Furthest Houses With Different Colors: house colors in a row."""


def check(colors: list[int]) -> None:
    assert 2 <= len(colors) <= 100, "2 <= n <= 100"
    assert all(0 <= c <= 100 for c in colors), "0 <= colors[i] <= 100"
    assert len(set(colors)) >= 2, "at least two houses have different colors"
