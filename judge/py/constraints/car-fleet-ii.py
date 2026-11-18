"""Car Fleet II: [position, speed] pairs with strictly increasing positions."""


def check(cars: list[list[int]]) -> None:
    assert isinstance(cars, list), "cars is a list"
    assert 1 <= len(cars) <= 10**5, "1 <= cars.length <= 10^5"
    assert all(isinstance(c, list) and len(c) == 2 for c in cars), "cars[i].length == 2"
    assert all(1 <= p <= 10**6 and 1 <= s <= 10**6 for p, s in cars), (
        "1 <= position[i], speed[i] <= 10^6"
    )
    assert all(cars[i][0] < cars[i + 1][0] for i in range(len(cars) - 1)), (
        "position[i] < position[i+1]"
    )
