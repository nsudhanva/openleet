"""Sort the People: names with distinct heights."""


def check(names: list[str], heights: list[int]) -> None:
    n = len(names)
    assert len(heights) == n, "n == names.length == heights.length"
    assert 1 <= n <= 10**3, "1 <= n <= 10^3"
    assert all(isinstance(s, str) and 1 <= len(s) <= 20 for s in names), (
        "1 <= names[i].length <= 20"
    )
    assert all(s.isascii() and s.isalpha() for s in names), (
        "names[i] consists of lower and upper case English letters"
    )
    assert all(isinstance(h, int) and 1 <= h <= 10**5 for h in heights), "1 <= heights[i] <= 10^5"
    assert len(set(heights)) == n, "all the values of heights are distinct"
