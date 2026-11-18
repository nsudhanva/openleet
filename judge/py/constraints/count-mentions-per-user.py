"""Count Mentions Per User: a user count and a list of MESSAGE/OFFLINE events."""


def check(numberOfUsers: int, events: list[list[str]]) -> None:
    assert 1 <= numberOfUsers <= 100, "1 <= numberOfUsers <= 100"
    assert 1 <= len(events) <= 100, "1 <= events.length <= 100"
    assert all(len(e) == 3 for e in events), "events[i].length == 3"
    assert all(e[0] in ("MESSAGE", "OFFLINE") for e in events), "events[i][0] is MESSAGE or OFFLINE"
    assert all(e[1].isdigit() and 1 <= int(e[1]) <= 10**5 for e in events), (
        "1 <= int(events[i][1]) <= 10^5"
    )
    for e in events:
        if e[0] == "OFFLINE":
            assert e[2].isdigit(), "OFFLINE event holds a user id"
            assert 0 <= int(e[2]) <= numberOfUsers - 1, "0 <= <number> <= numberOfUsers - 1"
        else:
            tokens = e[2].split(" ")
            if tokens in (["ALL"], ["HERE"]):
                continue
            assert all(t.startswith("id") and t[2:].isdigit() for t in tokens), (
                "mentions are id<number>, ALL or HERE"
            )
            assert 1 <= len(tokens) <= 100, "1 <= id mentions in a MESSAGE <= 100"
            assert all(0 <= int(t[2:]) <= numberOfUsers - 1 for t in tokens), (
                "0 <= <number> <= numberOfUsers - 1"
            )
    # status changes are processed before messages at the same timestamp
    offline_until: dict[int, int] = {}
    order = sorted((e for e in events if e[0] == "OFFLINE"), key=lambda e: int(e[1]))
    for e in order:
        uid, t = int(e[2]), int(e[1])
        assert offline_until.get(uid, 0) <= t, "OFFLINE user is online at that time"
        offline_until[uid] = t + 60
