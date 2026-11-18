"""Closest Room: [roomId, size] rooms and [preferred, minSize] queries."""


def check(rooms: list[list[int]], queries: list[list[int]]) -> None:
    assert 1 <= len(rooms) <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(queries) <= 10**4, "1 <= k <= 10^4"
    assert all(len(r) == 2 for r in rooms), "rooms[i] == [roomIdi, sizei]"
    assert all(len(q) == 2 for q in queries), "queries[j] == [preferredj, minSizej]"
    assert all(1 <= r <= 10**7 and 1 <= s <= 10**7 for r, s in rooms), "1 <= roomIdi, sizei <= 10^7"
    assert all(1 <= p <= 10**7 and 1 <= m <= 10**7 for p, m in queries), (
        "1 <= preferredj, minSizej <= 10^7"
    )
    assert len({r for r, _ in rooms}) == len(rooms), "each roomIdi is unique"
