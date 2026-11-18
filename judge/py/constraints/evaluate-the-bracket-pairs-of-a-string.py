"""Evaluate the Bracket Pairs of a String: a string with non-nested bracket pairs and a list of
unique key/value pairs."""


def check(s: str, knowledge: list[list[str]]) -> None:
    assert isinstance(s, str) and isinstance(knowledge, list), "s is a string, knowledge a list"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert 0 <= len(knowledge) <= 10**5, "0 <= knowledge.length <= 10^5"
    assert all(isinstance(p, list) and len(p) == 2 for p in knowledge), "knowledge[i].length == 2"
    assert all(1 <= len(k) <= 10 and 1 <= len(v) <= 10 for k, v in knowledge), (
        "1 <= keyi.length, valuei.length <= 10"
    )
    assert all(k.isascii() and k.islower() and k.isalpha() for k, _ in knowledge), (
        "keyi consists of lowercase English letters"
    )
    assert all(v.isascii() and v.islower() and v.isalpha() for _, v in knowledge), (
        "valuei consists of lowercase English letters"
    )
    assert len({k for k, _ in knowledge}) == len(knowledge), "each keyi in knowledge is unique"
    assert all(c == "(" or c == ")" or ("a" <= c <= "z") for c in s), (
        "s consists of lowercase English letters and round brackets"
    )
    inside = False
    key_len = 0
    for c in s:
        if c == "(":
            assert not inside, "there are no nested bracket pairs in s"
            inside = True
            key_len = 0
        elif c == ")":
            assert inside, "every close bracket has a corresponding open bracket"
            assert key_len > 0, "the key in each bracket pair of s is non-empty"
            inside = False
        else:
            key_len += 1
    assert not inside, "every open bracket '(' in s has a corresponding close bracket ')'"
