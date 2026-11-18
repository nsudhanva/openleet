"""Rectangle Area: two axis-aligned rectangles as corner coordinates."""


def check(ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int) -> None:
    assert -(10**4) <= ax1 <= ax2 <= 10**4, "-10^4 <= ax1 <= ax2 <= 10^4"
    assert -(10**4) <= ay1 <= ay2 <= 10**4, "-10^4 <= ay1 <= ay2 <= 10^4"
    assert -(10**4) <= bx1 <= bx2 <= 10**4, "-10^4 <= bx1 <= bx2 <= 10^4"
    assert -(10**4) <= by1 <= by2 <= 10**4, "-10^4 <= by1 <= by2 <= 10^4"
