"""Defanging an IP Address: a valid IPv4 address."""


def check(address: str) -> None:
    assert isinstance(address, str), "address is a string"
    parts = address.split(".")
    assert len(parts) == 4, "address is a valid IPv4 address (four parts)"
    for p in parts:
        assert p.isascii() and p.isdigit(), "address is a valid IPv4 address (digits)"
        assert 0 <= int(p) <= 255, "address is a valid IPv4 address (0..255)"
