"""Put Boxes Into the Warehouse: box heights and warehouse room heights."""


def check(boxes: list[int], warehouse: list[int]) -> None:
    assert isinstance(boxes, list) and isinstance(warehouse, list), "boxes and warehouse are arrays"
    assert 1 <= len(boxes) <= 10**5, "1 <= boxes.length <= 10^5"
    assert 1 <= len(warehouse) <= 10**5, "1 <= warehouse.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in boxes), "1 <= boxes[i] <= 10^9"
    assert all(1 <= v <= 10**9 for v in warehouse), "1 <= warehouse[i] <= 10^9"
