"""Solving Questions With Brainpower: [points, brainpower] pairs."""


def check(questions: list[list[int]]) -> None:
    assert 1 <= len(questions) <= 10**5, "1 <= questions.length <= 10^5"
    assert all(len(q) == 2 for q in questions), "questions[i].length == 2"
    assert all(1 <= v <= 10**5 for q in questions for v in q), "1 <= points, brainpower <= 10^5"
