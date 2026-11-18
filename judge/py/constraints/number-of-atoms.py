"""Number of Atoms: a valid chemical formula with letters, digits and parentheses."""


def check(formula: str) -> None:
    assert isinstance(formula, str), "formula is a string"
    assert 1 <= len(formula) <= 1000, "1 <= formula.length <= 1000"
    assert all(c.isascii() and (c.isalnum() or c in "()") for c in formula), (
        "formula consists of English letters, digits, '(', and ')'"
    )
    n = len(formula)
    i = 0
    stack: list[dict[str, int]] = [{}]
    prev_open = False
    while i < n:
        c = formula[i]
        i += 1
        if c == "(":
            stack.append({})
            prev_open = True
            continue
        if c == ")":
            assert len(stack) > 1, "formula is valid: balanced parentheses"
            assert not prev_open, "formula is valid: no empty parentheses"
            top = stack.pop()
            kind = "group"
        else:
            assert "A" <= c <= "Z", "formula is valid: an element starts with an uppercase letter"
            j = i
            while j < n and "a" <= formula[j] <= "z":
                j += 1
            name = formula[i - 1 : j]
            i = j
            top = {name: 1}
            kind = "atom"
        prev_open = False
        j = i
        while j < n and "0" <= formula[j] <= "9":
            j += 1
        if j > i:
            count = int(formula[i:j])
            assert count != 1, "a count of 1 is never written"
            assert count > 1, "a written count is greater than 1"
            top = {k: v * count for k, v in top.items()}
            i = j
        for k, v in top.items():
            stack[-1][k] = stack[-1].get(k, 0) + v
        assert kind in ("group", "atom")
    assert len(stack) == 1, "formula is valid: balanced parentheses"
    assert all(v < 2**31 for v in stack[0].values()), "output values fit in a 32-bit integer"
