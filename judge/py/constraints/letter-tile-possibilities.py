"""Letter Tile Possibilities: a string of uppercase letters."""


def check(tiles: str) -> None:
    assert 1 <= len(tiles) <= 7, "1 <= tiles.length <= 7"
    assert all("A" <= c <= "Z" for c in tiles), "tiles consists of uppercase English letters"
