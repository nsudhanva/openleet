"""Maximum Matching of Players With Trainers: player abilities and trainer capacities."""


def check(players: list[int], trainers: list[int]) -> None:
    assert 1 <= len(players) <= 10**5, "1 <= players.length <= 10^5"
    assert 1 <= len(trainers) <= 10**5, "1 <= trainers.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in players), "1 <= players[i] <= 10^9"
    assert all(1 <= v <= 10**9 for v in trainers), "1 <= trainers[j] <= 10^9"
