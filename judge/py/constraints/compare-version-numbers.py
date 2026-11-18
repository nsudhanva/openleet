"""Compare Version Numbers: two dot-separated version strings."""


def check(version1: str, version2: str) -> None:
    for name, v in (("version1", version1), ("version2", version2)):
        assert isinstance(v, str), f"{name} is a string"
        assert 1 <= len(v) <= 500, f"1 <= {name}.length <= 500"
        assert all((c.isdigit() and c.isascii()) or c == "." for c in v), (
            f"{name} only contains digits and '.'"
        )
        revisions = v.split(".")
        assert all(r != "" for r in revisions), f"{name} is a valid version number"
        assert all(int(r) < 2**31 for r in revisions), f"{name} revisions fit in a 32-bit integer"
