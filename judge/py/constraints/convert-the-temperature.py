"""Convert the Temperature: a Celsius temperature."""


def check(celsius: float) -> None:
    assert isinstance(celsius, (int, float)), "celsius is a number"
    assert 0 <= celsius <= 1000, "0 <= celsius <= 1000"
    assert abs(celsius * 100 - round(celsius * 100)) < 1e-6, (
        "celsius is rounded to two decimal places"
    )
