"""Construct Binary Tree from String: an integer with nested parenthesized subtrees."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    n = len(s)
    assert 0 <= n <= 3 * 10**4, "0 <= s.length <= 3 * 10^4"
    assert all(c in "0123456789()-" for c in s), "s consists of digits, '(', ')', and '-' only"
    if n == 0:
        return

    def number(i: int) -> int:
        j = i + 1 if i < n and s[i] == "-" else i
        k = j
        while k < n and s[k].isdigit():
            k += 1
        assert k > j, "each node starts with an integer"
        digits = s[j:k].lstrip("0")
        assert len(digits) <= 10 and int(digits or "0") <= 2**30, (
            "All numbers in the tree have value at most 2^30"
        )
        return k

    # Grammar: node := integer [ "(" node ")" ] [ "(" node ")" ]
    i = number(0)
    children = [0]
    while i < n:
        if s[i] == "(":
            assert children[-1] < 2, "a node has at most two children"
            children[-1] += 1
            children.append(0)
            i = number(i + 1)
        else:
            assert s[i] == ")" and len(children) > 1, "parentheses are balanced"
            children.pop()
            i += 1
    assert len(children) == 1, "parentheses are balanced"
