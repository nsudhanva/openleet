"""Maximum Units on a Truck: box types as [count, units per box] and a truck size."""


def check(boxTypes: list[list[int]], truckSize: int) -> None:
    assert 1 <= len(boxTypes) <= 1000, "1 <= boxTypes.length <= 1000"
    assert all(len(b) == 2 for b in boxTypes), "boxTypes[i].length == 2"
    assert all(1 <= a <= 1000 and 1 <= u <= 1000 for a, u in boxTypes), (
        "1 <= numberOfBoxesi, numberOfUnitsPerBoxi <= 1000"
    )
    assert 1 <= truckSize <= 10**6, "1 <= truckSize <= 10^6"
