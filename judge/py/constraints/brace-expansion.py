"""Brace Expansion: a string of letters and non-nested {a,b,...} option groups."""

from string import ascii_lowercase

_LOWER = set(ascii_lowercase)


def check(s: str) -> None:
    assert 1 <= len(s) <= 50, "1 <= s.length <= 50"
    assert set(s) <= _LOWER | set("{},"), "s consists of '{}', ',' and lowercase English letters"
    group = None
    after_letter = False  # inside a group: the last token was an option letter
    for c in s:
        if c == "{":
            assert group is None, "no nested curly brackets"
            group, after_letter = [], False
        elif c == "}":
            assert group is not None, "s is a valid input: braces are balanced"
            assert after_letter, "s is a valid input: options are non-empty letters"
            assert len(set(group)) == len(group), (
                "characters inside a pair of curly brackets are different"
            )
            group = None
        elif c == ",":
            assert group is not None, "s is a valid input: commas only inside braces"
            assert after_letter, "s is a valid input: options are non-empty letters"
            after_letter = False
        elif group is not None:
            assert not after_letter, "s is a valid input: each option is one letter"
            group.append(c)
            after_letter = True
    assert group is None, "s is a valid input: braces are balanced"
