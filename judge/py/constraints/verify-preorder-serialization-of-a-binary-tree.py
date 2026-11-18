"""Verify Preorder Serialization of a Binary Tree: comma-separated integers and '#'."""


def check(preorder: str) -> None:
    assert 1 <= len(preorder) <= 10**4, "1 <= preorder.length <= 10^4"
    for tok in preorder.split(","):
        assert tok == "#" or (tok.isascii() and tok.isdigit() and 0 <= int(tok) <= 100), (
            "each value is an integer in [0, 100] or '#', separated by single commas"
        )
