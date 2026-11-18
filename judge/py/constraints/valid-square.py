"""Valid Square: four points given as [x, y] pairs."""


def check(p1: list[int], p2: list[int], p3: list[int], p4: list[int]) -> None:
    pts = [p1, p2, p3, p4]
    assert all(isinstance(p, list) and len(p) == 2 for p in pts), (
        "p1.length == p2.length == p3.length == p4.length == 2"
    )
    assert all(-(10**4) <= v <= 10**4 for p in pts for v in p), "-10^4 <= xi, yi <= 10^4"
