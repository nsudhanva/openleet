"""The Score of Students Solving Math Expression: a single-digit +/* expression and a list of
student answers."""


def check(s: str, answers: list[int]) -> None:
    assert isinstance(s, str) and 3 <= len(s) <= 31, "3 <= s.length <= 31"
    assert len(s) % 2 == 1, "s is a valid expression (operands alternate with operators)"
    assert all(c in "0123456789" for c in s[0::2]), "operands are digits in [0, 9]"
    assert all(c in "+*" for c in s[1::2]), "s contains only digits, '+' and '*'"
    ops = len(s) // 2
    assert 1 <= ops <= 15, "1 <= operator count <= 15"
    total, product = 0, int(s[0])
    assert product <= 10**9, "intermediate products <= 10^9"
    for op, d in zip(s[1::2], s[2::2], strict=True):
        if op == "*":
            product *= int(d)
            assert product <= 10**9, "intermediate products <= 10^9"
        else:
            total += product
            product = int(d)
    total += product
    assert 0 <= total <= 1000, "correct answer is in [0, 1000]"
    assert 1 <= len(answers) <= 10**4, "1 <= n <= 10^4"
    assert all(0 <= a <= 1000 for a in answers), "0 <= answers[i] <= 1000"
