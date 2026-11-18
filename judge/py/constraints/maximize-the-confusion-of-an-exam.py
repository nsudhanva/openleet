"""Maximize the Confusion of an Exam: a string of 'T'/'F' answers and k."""


def check(answerKey: str, k: int) -> None:
    n = len(answerKey)
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert set(answerKey) <= {"T", "F"}, "answerKey[i] is either 'T' or 'F'"
    assert 1 <= k <= n, "1 <= k <= n"
