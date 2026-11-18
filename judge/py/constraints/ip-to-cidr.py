"""IP to CIDR: an IPv4 start address and a count of addresses."""


def check(ip: str, n: int) -> None:
    assert isinstance(ip, str), "ip is a string"
    assert 7 <= len(ip) <= 15, "7 <= ip.length <= 15"
    parts = ip.split(".")
    assert len(parts) == 4, 'ip has the form "a.b.c.d"'
    assert all(p.isascii() and p.isdigit() for p in parts), "a, b, c, d are integers"
    assert all(0 <= int(p) <= 255 for p in parts), "a, b, c, d in [0, 255]"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    start = sum(int(p) << s for p, s in zip(parts, (24, 16, 8, 0), strict=True))
    assert start + n - 1 <= 2**32 - 1, (
        "every implied address ip + x (x < n) is a valid IPv4 address"
    )
