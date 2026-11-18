"""Decode String: a valid encoded string of lowercase letters, k[...] groups and brackets."""

import string


def check(s: str) -> None:
    assert 1 <= len(s) <= 30, "1 <= s.length <= 30"
    allowed = set(string.ascii_lowercase + string.digits + "[]")
    assert set(s) <= allowed, "s consists of lowercase English letters, digits, and square brackets"
    stack = [0]  # length of the decoded text at each open level
    mult: list[int] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            assert j < len(s) and s[j] == "[", "digits are only repeat counts followed by '['"
            k = int(s[i:j])
            assert 1 <= k <= 300, "all the integers in s are in the range [1, 300]"
            mult.append(k)
            stack.append(0)
            i = j + 1
            continue
        if c == "[":
            raise AssertionError("every '[' follows a repeat count")
        if c == "]":
            assert mult, "square brackets are well-formed"
            inner = stack.pop()
            stack[-1] += inner * mult.pop()
            assert stack[-1] <= 10**5, "the decoded length never exceeds 10^5"
        else:
            stack[-1] += 1
        i += 1
    assert not mult, "square brackets are well-formed"
    assert stack[0] <= 10**5, "the decoded length never exceeds 10^5"
