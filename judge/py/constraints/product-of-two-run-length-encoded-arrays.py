"""Product of Two Run-Length Encoded Arrays: two run-length encodings of equal total length."""


def check(encoded1: list[list[int]], encoded2: list[list[int]]) -> None:
    for name, enc in (("encoded1", encoded1), ("encoded2", encoded2)):
        assert isinstance(enc, list), f"{name} is an array"
        assert 1 <= len(enc) <= 10**5, f"1 <= {name}.length <= 10^5"
        assert all(isinstance(p, list) and len(p) == 2 for p in enc), f"{name}[i].length == 2"
        assert all(1 <= v <= 10**4 and 1 <= f <= 10**4 for v, f in enc), "1 <= val, freq <= 10^4"
    assert sum(f for _, f in encoded1) == sum(f for _, f in encoded2), (
        "the full arrays are the same length"
    )
