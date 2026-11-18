"""Find Words That Can Be Formed by Characters: lowercase words and a lowercase string."""


def check(words: list[str], chars: str) -> None:
    assert 1 <= len(words) <= 1000, "1 <= words.length <= 1000"
    assert all(1 <= len(w) <= 100 for w in words), "1 <= words[i].length <= 100"
    assert 1 <= len(chars) <= 100, "1 <= chars.length <= 100"
    assert all(c.isascii() and c.islower() for c in chars + "".join(words)), (
        "words[i] and chars consist of lowercase English letters"
    )
