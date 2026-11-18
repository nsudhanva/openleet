"""Minimize Result by Adding Parentheses to Expression: "<num1>+<num2>" with digits 1-9."""


def check(expression: str) -> None:
    assert 3 <= len(expression) <= 10, "3 <= expression.length <= 10"
    assert all(c in "123456789+" for c in expression), (
        "expression consists of digits from '1' to '9' and '+'"
    )
    assert expression.count("+") == 1, "expression contains exactly one '+'"
    assert expression[0] != "+" and expression[-1] != "+", "expression starts and ends with digits"
    left, right = expression.split("+")
    a, b = int(left), int(right)
    limit = 2**31 - 1
    assert a + b <= limit, "the original value fits within a signed 32-bit integer"
    for i in range(len(left)):
        for j in range(1, len(right) + 1):
            pre = int(left[:i]) if i else 1
            mid_l = int(left[i:])
            mid_r = int(right[:j])
            post = int(right[j:]) if j < len(right) else 1
            assert pre * (mid_l + mid_r) * post <= limit, (
                "the value after adding parentheses fits within a signed 32-bit integer"
            )
