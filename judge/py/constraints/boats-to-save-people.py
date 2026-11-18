"""Boats to Save People: people's weights and a boat weight limit."""


def check(people: list[int], limit: int) -> None:
    assert 1 <= len(people) <= 5 * 10**4, "1 <= people.length <= 5 * 10^4"
    assert 1 <= limit <= 3 * 10**4, "limit <= 3 * 10^4"
    assert all(1 <= p <= limit for p in people), "1 <= people[i] <= limit"
