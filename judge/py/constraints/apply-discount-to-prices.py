"""Apply Discount to Prices: a sentence of single-space separated words and a discount."""


def check(sentence: str, discount: int) -> None:
    assert 1 <= len(sentence) <= 10**5, "1 <= sentence.length <= 10^5"
    assert all(c.isascii() and (c.islower() or c.isdigit() or c in " $") for c in sentence), (
        "sentence consists of lowercase English letters, digits, ' ', and '$'"
    )
    assert sentence == sentence.strip(" "), "sentence does not have leading or trailing spaces"
    assert "  " not in sentence, "All words in sentence are separated by a single space"
    for word in sentence.split(" "):
        if len(word) > 1 and word[0] == "$" and all(c in "0123456789" for c in word[1:]):
            assert word[1] != "0", "All prices will be positive numbers without leading zeros"
            assert len(word) - 1 <= 10, "All prices will have at most 10 digits"
    assert 0 <= discount <= 100, "0 <= discount <= 100"
