"""Stickers to Spell Word: lowercase sticker words and a lowercase target."""


def check(stickers: list[str], target: str) -> None:
    assert 1 <= len(stickers) <= 50, "1 <= n <= 50"
    assert all(isinstance(s, str) for s in stickers), "stickers[i] is a string"
    assert all(1 <= len(s) <= 10 for s in stickers), "1 <= stickers[i].length <= 10"
    assert isinstance(target, str) and 1 <= len(target) <= 15, "1 <= target.length <= 15"
    assert all("a" <= c <= "z" for s in [*stickers, target] for c in s), (
        "stickers[i] and target consist of lowercase English letters"
    )
