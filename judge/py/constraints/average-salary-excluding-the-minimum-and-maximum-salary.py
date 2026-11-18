"""Average Salary Excluding the Minimum and Maximum Salary: unique salaries."""


def check(salary: list[int]) -> None:
    assert 3 <= len(salary) <= 100, "3 <= salary.length <= 100"
    assert all(1000 <= v <= 10**6 for v in salary), "1000 <= salary[i] <= 10^6"
    assert len(set(salary)) == len(salary), "all the integers of salary are unique"
