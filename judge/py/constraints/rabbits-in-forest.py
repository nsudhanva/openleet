"""Rabbits in Forest: an array of rabbit answers."""


def check(answers: list[int]) -> None:
    assert isinstance(answers, list), "answers is an array"
    assert 1 <= len(answers) <= 1000, "1 <= answers.length <= 1000"
    assert all(0 <= a < 1000 for a in answers), "0 <= answers[i] < 1000"
